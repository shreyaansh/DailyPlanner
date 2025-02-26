import json
import re
from datetime import datetime, timedelta

def extract_json(text):
    print("Extracting JSON from the text...")
    print("Text to extract JSON from:")
    print(text)
    json_pattern = r"\{.*\}|\[.*\]"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            print("Extracted text is not valid JSON.")
            return None
    else:
        print("No JSON found in the text.")
        return None

def fix_json(json_str):
    json_str = extract_json(json_str)
    if json_str is None:
        print("No JSON found in the text.")
        return None
    pattern = r"(?<!\\)'(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"
    json_str = re.sub(pattern, '"', json_str)
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)
    json_str = re.sub(r'\)\s*$', '}', json_str)
    return json_str

def get_current_date():
    today = datetime.today()
    date_str = today.strftime("%d-%m-%Y")
    return date_str

def get_current_week():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_week_str = start_of_week.strftime("%d-%m-%Y")
    end_of_week_str = end_of_week.strftime("%d-%m-%Y")
    return '"' + start_of_week_str + "||" + end_of_week_str + '"'