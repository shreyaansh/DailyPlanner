from openai import OpenAI
from google import generativeai as genai
from string import Template
from dotenv import load_dotenv
import os
import tiktoken
from meal_plan_generator.meal_plan_generator import generate_meal_plan_week
from db.db import get_mongo_client

load_dotenv()

# Create a new client and connect to the server
client = get_mongo_client()

gpt_api_key = os.getenv("OPENAI_API_KEY")  # Replace with your OpenAI API key
gpt_client = OpenAI(api_key=gpt_api_key)

gemini_api_key = os.getenv("GEMINI_API_KEY")  # Replace with your Google API key
genai.configure(api_key=gemini_api_key)

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

def main():
    print("Welcome to DailyPlanner!")
    print("Generating your weekly meal plan...")
    generate_meal_plan_week("gpt-4")
    print("Meal plans generated and saved to files.")

if __name__ == "__main__":
    main()