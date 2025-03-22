import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Step 1: Read the CSV file into a pandas DataFrame
df = pd.read_csv('resources/food.csv')