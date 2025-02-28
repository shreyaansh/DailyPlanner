import json
import random
from string import Template
from google import generativeai as genai
from db.db import insert_meal_plan_into_db
from ai.models import call_model
from utils.utils import extract_json, fix_json, get_current_date, get_current_week

cuisines = ["Punjabi", "Telugu", "Italian", "Thai", "Bengali", "Moroccan", "Korean"]

def generate_meal_plan_day(day, date, cuisine, week, model):
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
                        {"person": "Person 2", "size": "quantity", "calories": "number", "protein": "number", "fat": "number", "carbs": "number", "fiber": "number"}
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

    prompt_for_day = prompt.substitute(day=day, date=date, cuisine=cuisine, week=week)
    response_text = call_model(prompt_for_day, model)

    try:
        response_text = extract_json(response_text)
        response_text = fix_json(response_text)
        if response_text is None:
            print("No JSON found in the response.")
            return None

        meal_plan = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}\n")
        print("Response text:", response_text)

    return meal_plan

def generate_meal_plan_week(model):
    week = get_current_week()
    date = get_current_date()
    json_string = ""

    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        random.shuffle(cuisines)
        cuisine = cuisines[0]
        meal_plan = generate_meal_plan_day(day, date, cuisine, week, model)

        if meal_plan is not None:
            print(f"Meal plan for {day} generated successfully.")
        else:
            print(f"Failed to generate meal plan for {day}.")
            return None

        if json_string == "":
            json_string = json.dumps(meal_plan, indent=4)
        else:
            json_string = json_string + ",\n" + json.dumps(meal_plan, indent=4)

    json_string = "[" + json_string + "]"
    json_string = "{ " + week + " : " + json_string + " }"
    json_obj = json.loads(json_string)

    insert_meal_plan_into_db(json_obj, model)