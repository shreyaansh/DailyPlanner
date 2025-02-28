from google import generativeai as genai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

gpt_api_key = os.getenv("OPENAI_API_KEY")  # Replace with your OpenAI API key
gpt_client = OpenAI(api_key=gpt_api_key)

gemini_api_key = os.getenv("GEMINI_API_KEY")  # Replace with your Google API key
genai.configure(api_key=gemini_api_key)

def call_model(prompt, model_name):
    print(f"Calling model: {model_name}")
    if 'gemini' in model_name:
        # Use the Gemini model to generate content
        gemini_model = genai.GenerativeModel(model_name)
        response = gemini_model.generate_content(prompt)
        return response.text
    elif 'gpt' in model_name:
        response = gpt_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a nutritionist and a chef. You are an expert in creating meal plans for people with different dietary needs and preferences."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    else:
        raise ValueError(f"Unknown model name: {model_name}")