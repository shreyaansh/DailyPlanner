from openai import OpenAI
from google import generativeai as genai
from string import Template
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import os
import random
import re
import tiktoken


load_dotenv()

gpt_api_key = os.getenv("OPENAI_API_KEY")  # Replace with your OpenAI API key

gpt_client = OpenAI(
  api_key=gpt_api_key
)

gemini_api_key = os.getenv("GEMINI_API_KEY")  # Replace with your Google API key
genai.configure(api_key = gemini_api_key)

# Select the Gemini Ultra model
model = genai.GenerativeModel('gemini-1.5-pro')

cuisines = ["Punjabi", "Telugu", "Italian", "Thai", "Bengali", "Moroccan", "Korean"]

def get_token_count(text):
    """
    Function to count the number of tokens in a given text.
    Uses the tiktoken library to encode the text and count the tokens.
    """
    # Initialize the tokenizer for the model you're using
    encoding = tiktoken.encoding_for_model('gpt-4')
    
    # Encode the text
    tokens = encoding.encode(text)
    
    print(f"Number of tokens: {len(tokens)}")


# Function to extract JSON from a string
def extract_json(text):
    """
    Extracts JSON from a string that may contain additional text.
    """

    print("Extracting JSON from the text...")
    print("Text to extract JSON from:")
    print(text)

    # Regex to match JSON objects or arrays
    json_pattern = r"\{.*\}|\[.*\]"
    
    # Search for JSON in the text
    match = re.search(json_pattern, text, re.DOTALL)
    
    if match:
        json_str = match.group(0)
        try:
            # Validate the JSON
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            print("Extracted text is not valid JSON.")
            return None
    else:
        print("No JSON found in the text.")
        return None


# Function to fix JSON
def fix_json(json_str : str):
    # Extract JSON from the string
    json_str = extract_json(json_str)

    if json_str is None:
        print("No JSON found in the text.")
        return None

    # Replaces single quotes with double quotes, but skips single quotes inside double-quoted strings.
    # Regex pattern to match single quotes outside of double-quoted strings
    pattern = r"(?<!\\)'(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"
    # Replace single quotes with double quotes
    json_str = re.sub(pattern, '"', json_str)
    
    # Remove trailing commas
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)

    # Replace ')' with '}' if it appears at the end of a JSON object
    json_str = re.sub(r'\)\s*$', '}', json_str)
    
    return json_str


# Function to generate a meal plan for a specific day
def generate_meal_plan_day(day : str, date : str, cuisine : str, week : str):
    # Define the prompt
    prompt = Template("""
        Generate a weekly meal plan for 2 people in JSON format. The meal plan should include:
        - A breakdown for the day:
        - Meal type (e.g., Breakfast, Lunch, Dinner).
        - Recipe name.
        - Macros (calories, protein, fat, carbs, fiber) for the total dish.
        - Portion sizes for each person.

        Constraints:
        - Daily calorie goal: SB has a resting metabolic rate of 2000 calories per day, SD has a resting metabolic rate of 1400 calories per day.
        - Minimum protein: SB 130g, SD 100g.
        - Intent to lose fat and build muscle mass.
        - Reach daily recommended fiber intake (SB: 40g, SD: 30g).
        - Meals: Breakfast, Lunch and dinner, 2 snacks.
        - Avoid repetitive meals.
        - Ensure the plan is balanced and nutritious.
        - SB and SD both work out 4-5 times a week, so the meal plan should be designed to support their active lifestyle.
        - SB is 5'5" and weighs 160 lbs and is male, SD is 5'6" and weighs 134 lbs and is female. Both are 28 years old.
        - IMPORTANT: Snacks can be scattered in between and can be used as needed to increase daily intake based on activity level.
        - IMPORTANT: (SD doesn't like fruits, so only include fruits in SB's meals)
        - IMPORTANT: Avoid grilled meats, and if Telugu cuisine is selected, avoid using dosas in the meal plan.
        - IMPORTANT: Stick to using proteins like chicken, salmon, ground turkey, paneer, tofu, legumes, and lentils.
        - IMPORTANT: Bonus if the meal plan local recipes include veggies like spinach, broccoli, kale, and other leafy greens.
        - IMPORTANT: When formulating a day plan, stick to the $cuisine. Use the name of the actual dish in the recipe name in the json.

        Return the data in the following JSON structure:
        {
            "week": "$week",
            "day": "$day",
            "date": "$date",
            "cuisine": "$cuisine",
            "total macros": [{"person": "person1", "calories": number, "protein": number, "fat": number, "carbs": number, "fiber": number},
                            {"person": "person2", "calories": number, "protein": number, "fat": number, "carbs": number, "fiber": number}],
            "meals": [
                {
                    "meal_type": "Breakfast",
                    "recipe": "Recipe Name in local language from the $cuisine cuisine",
                    "macros": {"calories": number, "protein": number, "fat": number, "carbohydrates": number, "fiber": number},
                    "portions": [
                        {"person": "Person 1", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"},
                        {"person": "Person 2", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"}
                    ],
                },
                {
                    "meal_type": "Snack 1",
                    "recipe": "Recipe Name in local language from the $cuisine cuisine",
                    "macros": {"calories": number, "protein": number, "fat": number, "carbohydrates": number, "fiber": number},
                    "portions": [
                        {"person": "Person 1", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"},
                        {"person": "Person 2", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"}
                    ],
                },
                {
                    "meal_type": "Lunch",
                    "recipe": "Recipe Name in local language from the $cuisine cuisine",
                    "macros": {"calories": number, "protein": number, "fat": number, "carbohydrates": number, "fiber": number},
                    "portions": [
                        {"person": "Person 1", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"},
                        {"person": "Person 2", "size": "quantity, "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number""}
                    ],
                },
                {
                    "meal_type": "Snack 2",
                    "recipe": "Recipe Name in local language from the $cuisine cuisine",
                    "macros": {"calories": number, "protein": number, "fat": number, "carbohydrates": number, "fiber": number},
                    "portions": [
                        {"person": "Person 1", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"},
                        {"person": "Person 2", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"}
                    ],
                },
                {
                    "meal_type": "Dinner",
                    "recipe": "Recipe Name in local language from the $cuisine cuisine",
                    "macros": {"calories": number, "protein": number, "fat": number, "carbohydrates": number, "fiber": number},
                    "portions": [
                        {"person": "Person 1", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"},
                        {"person": "Person 2", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"}
                    ],
                },
            ]
        }
        IMPORTANT: Do not include any additional text or explanations.
        IMPORTANT: Return ONLY valid JSON.
    """)

    # Generate the meal plan for the day
    prompt_for_day = prompt.substitute(day=day, date=date, cuisine=cuisine, week=week)

    # Call the Gemini API
    # response = gemini_client.generate_content(
    #     model="gemini-1.5-pro",
    #     prompt=prompt_for_day,
    #     temperature=0.5,
    #     max_output_tokens=2000
    # )
    # # Extract the JSON from the response
    # response_text = response.candidates[0].content


    # Call the OpenAI API
    # response = gpt_client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You are a nutritionist and meal planner who creates detailed meal plans in JSON format."},
    #         {"role": "user", "content": prompt_for_day}
    #     ]
    # )

    # Call the Gemini API
    response_gemini = model.generate_content(
        prompt_for_day
    )

    # Extract the JSON from the response
    gemini_response_text = response_gemini.text

    try:
        if gemini_response_text is not None:
            # Validate the JSON
            response_text = extract_json(gemini_response_text)
            response_text = fix_json(response_text) # Fix the JSON
            if response_text is None:
                print("No JSON found in the response.")
                return None
        else:
            response_text = response.choices[0].message.content # Extract the JSON from the response
            response_text = fix_json(response_text) # Fix the JSON
            if response_text is None:
                print("No JSON found in the response.")
                return None
        meal_plan = json.loads(response_text) # Load the JSON into a Python object
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}\n")
        print("Response text:", response_text)

    return meal_plan


def get_current_date():
    # Get the current date
    today = datetime.today()

    # Format the date as a string
    date_str = today.strftime("%d-%m-%Y")

    return date_str

def get_current_week():
    # Get the current date
    today = datetime.today()
    
    # Calculate the start of the week (Monday)
    start_of_week = today - timedelta(days=today.weekday())

    # Calculate the end of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)

    #Format the dates as strings
    start_of_week_str = start_of_week.strftime("%d-%m-%Y")
    end_of_week_str = end_of_week.strftime("%d-%m-%Y")

    # Return the start and end of the week
    return ('"' + start_of_week_str + "||" + end_of_week_str + '"')


# Function to generate a meal plan for the week
def generate_meal_plan_week():
    # Get the current week
    week = get_current_week()
    date = get_current_date()

    json_string = ""

    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        random.shuffle(cuisines)
        cuisine = cuisines[0]  # Randomly select a cuisine for the day
        meal_plan = generate_meal_plan_day(day, date, cuisine, week)
        
        if meal_plan is not None:
            print(f"Meal plan for {day} generated successfully.")
        else:
            print(f"Failed to generate meal plan for {day}.")
            return None
        # Save the meal plan to a file, append it to the file name with the day of the week
        if (json_string == ""):
            json_string = json.dumps(meal_plan, indent=4)
        else:
            json_string = json_string + ",\n" + json.dumps(meal_plan, indent=4)

    # Convert the json_string to a valid JSON array
    json_string = "[" + json_string + "]"

    # Add the week to the JSON string as the key
    json_string = "{ " + week + " : " + json_string + " }"

    json_obj = json.loads(json_string)
    
    # Save the JSON string to a file
    with open("meal_plan_gemini1.json", "w") as f:
        json.dump(json_obj, f, indent=4)


def main():
    print("Welcome to DailyPlanner!")

    print("Generating your weekly meal plan...")
    generate_meal_plan_week()

    print("Meal plans generated and saved to files.")

if __name__ == "__main__":
    main()