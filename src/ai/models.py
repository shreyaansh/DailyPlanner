from google import generativeai as genai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

gpt_api_key = os.getenv("OPENAI_API_KEY")  # Replace with your OpenAI API key
gpt_client = OpenAI(api_key=gpt_api_key)

gemini_api_key = os.getenv("GEMINI_API_KEY")  # Replace with your Google API key
genai.configure(api_key=gemini_api_key)

# Select the Gemini Ultra model
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

def call_model(prompt, model_name):
    if model_name == 'gemini':
        response = gemini_model.generate_content(prompt)
        return response.text
    elif model_name == 'gpt':
        response = gpt_client.Completion.create(
            engine="gpt-4o",
            prompt=prompt,
        )
        return response.choices[0].text
    else:
        raise ValueError(f"Unknown model name: {model_name}")