from db.db import get_mongo_client

def retrieve_meal_plans():
    client = get_mongo_client()
    db = client['meal_plans']
    collection = db['weekly_plans']
    
    # Retrieve the meal plans from the database
    meal_plans = collection.find()
    
    return meal_plans

# Define the scoring system for each metric
def score_difficulty(difficulty_level):
    """Assign a score based on difficulty level."""
    difficulty_scores = {1: "Very Easy", 2: "Easy", 3: "Moderate", 4: "Difficult", 5: "Very Difficult"}
    return difficulty_level  # Return the numeric score

def score_variety(uniqueness_percent):
    """Score variety as a percentage of uniqueness."""
    return uniqueness_percent  # The percentage of variety (0 to 100)

# Example of scoring healthiness based on nutrition data
def score_healthiness(nutrition_data):
    """Score healthiness based on nutritional values."""
    protein_score = 0
    fat_score = 0
    carb_score = 0
    fiber_score = 0
    sodium_sugar_score = 0
    micronutrient_score = 0

    # Protein: Aim for 20g or more per meal
    if nutrition_data['protein'] >= 30:
        protein_score = 5
    elif nutrition_data['protein'] >= 20:
        protein_score = 4
    elif nutrition_data['protein'] >= 10:
        protein_score = 3
    elif nutrition_data['protein'] >= 5:
        protein_score = 2
    else:
        protein_score = 1

    # Fat Composition: Favor healthy fats
    if nutrition_data['fat_source'] == 'healthy':
        fat_score = 5
    elif nutrition_data['fat_source'] == 'moderate':
        fat_score = 4
    elif nutrition_data['fat_source'] == 'unhealthy':
        fat_score = 2
    else:
        fat_score = 1

    # Carbohydrates: Prefer complex carbs
    if nutrition_data['carbs'] == 'complex':
        carb_score = 5
    elif nutrition_data['carbs'] == 'balanced':
        carb_score = 4
    elif nutrition_data['carbs'] == 'simple':
        carb_score = 3
    else:
        carb_score = 1

    # Fiber: Aim for ≥10g of fiber
    if nutrition_data['fiber'] >= 10:
        fiber_score = 5
    elif nutrition_data['fiber'] >= 7:
        fiber_score = 4
    elif nutrition_data['fiber'] >= 4:
        fiber_score = 3
    elif nutrition_data['fiber'] >= 2:
        fiber_score = 2
    else:
        fiber_score = 1

    # Sodium and Sugar: Prefer low amounts of both
    if nutrition_data['sodium'] < 300 and nutrition_data['sugar'] < 5:
        sodium_sugar_score = 5
    elif nutrition_data['sodium'] < 500 and nutrition_data['sugar'] < 10:
        sodium_sugar_score = 4
    elif nutrition_data['sodium'] < 1000 and nutrition_data['sugar'] < 15:
        sodium_sugar_score = 3
    elif nutrition_data['sodium'] < 1500 and nutrition_data['sugar'] < 20:
        sodium_sugar_score = 2
    else:
        sodium_sugar_score = 1

    # Micronutrient Density: Score based on variety and nutrient-rich foods
    if nutrition_data['micronutrients'] == 'high':
        micronutrient_score = 5
    elif nutrition_data['micronutrients'] == 'moderate':
        micronutrient_score = 4
    elif nutrition_data['micronutrients'] == 'low':
        micronutrient_score = 3
    else:
        micronutrient_score = 1

    # Return total health score
    health_score = sum([protein_score, fat_score, carb_score, fiber_score, sodium_sugar_score, micronutrient_score])
    return health_score

# Example nutrition data for a meal
nutrition_data = {
    'protein': 25,  # in grams
    'fat_source': 'healthy',
    'carbs': 'complex',
    'fiber': 8,  # in grams
    'sodium': 350,  # in mg
    'sugar': 3,  # in grams
    'micronutrients': 'high'  # indicates nutrient-rich ingredients like greens, fruits
}

# Calculate healthiness score
healthiness_score = score_healthiness(nutrition_data)
print(f"Healthiness Score: {healthiness_score}")


def score_healthiness(nutrition_data):
    """Score healthiness on a scale of 1 to 5."""
    # Example of scoring healthiness based on nutrition data
    """Score healthiness based on nutritional values."""
    protein_score = 0
    fat_score = 0
    carb_score = 0
    fiber_score = 0
    sodium_sugar_score = 0
    micronutrient_score = 0

    # Protein: Aim for 20g or more per meal
    if nutrition_data['protein'] >= 30:
        protein_score = 5
    elif nutrition_data['protein'] >= 20:
        protein_score = 4
    elif nutrition_data['protein'] >= 10:
        protein_score = 3
    elif nutrition_data['protein'] >= 5:
        protein_score = 2
    else:
        protein_score = 1

    # Fat Composition: Favor healthy fats
    if nutrition_data['fat_source'] == 'healthy':
        fat_score = 5
    elif nutrition_data['fat_source'] == 'moderate':
        fat_score = 4
    elif nutrition_data['fat_source'] == 'unhealthy':
        fat_score = 2
    else:
        fat_score = 1

    # Carbohydrates: Prefer complex carbs
    if nutrition_data['carbs'] == 'complex':
        carb_score = 5
    elif nutrition_data['carbs'] == 'balanced':
        carb_score = 4
    elif nutrition_data['carbs'] == 'simple':
        carb_score = 3
    else:
        carb_score = 1

    # Fiber: Aim for ≥10g of fiber
    if nutrition_data['fiber'] >= 10:
        fiber_score = 5
    elif nutrition_data['fiber'] >= 7:
        fiber_score = 4
    elif nutrition_data['fiber'] >= 4:
        fiber_score = 3
    elif nutrition_data['fiber'] >= 2:
        fiber_score = 2
    else:
        fiber_score = 1

        # Sodium: Score based on sodium content
    if nutrition_data['sodium'] < 300:
        sodium_score = 5
    elif nutrition_data['sodium'] < 500:
        sodium_score = 4
    elif nutrition_data['sodium'] < 1000:
        sodium_score = 3
    elif nutrition_data['sodium'] < 1500:
        sodium_score = 2
    else:
        sodium_score = 1

    # Sugar: Score based on sugar content
    if nutrition_data['sugar'] < 5:
        sugar_score = 5
    elif nutrition_data['sugar'] < 10:
        sugar_score = 4
    elif nutrition_data['sugar'] < 15:
        sugar_score = 3
    elif nutrition_data['sugar'] < 20:
        sugar_score = 2
    else:
        sugar_score = 1

    # Micronutrient Density: Score based on variety and nutrient-rich foods
    if nutrition_data['micronutrients'] == 'high':
        micronutrient_score = 5
    elif nutrition_data['micronutrients'] == 'moderate':
        micronutrient_score = 4
    elif nutrition_data['micronutrients'] == 'low':
        micronutrient_score = 3
    else:
        micronutrient_score = 1

    # Return total health score
    health_score = sum([protein_score, fat_score, carb_score, fiber_score, sodium_score, sugar_score, micronutrient_score])

    # # Calculate healthiness score
    # healthiness_score = score_healthiness(nutrition_data)
    # print(f"Healthiness Score: {healthiness_score}")

    return health_score

def score_nutrient_balance(nutrient_balance_percent):
    """Score how balanced the nutrients are."""
    return nutrient_balance_percent  # Nutrient balance from 0 to 100%

def score_customization(customization_percent):
    """Score based on how well it fits user preferences."""
    return customization_percent  # Customization from 0 to 100%

def score_satisfaction(satisfaction_rating):
    """User satisfaction on a scale of 1 to 5."""
    return satisfaction_rating

def score_time_cost_efficiency(time_cost_percent):
    """Score how time and cost efficient the meal plan is."""
    return time_cost_percent  # Efficiency from 0 to 100%

def score_predictive_performance(predictive_percent):
    """Score based on how likely meals are to be prepared."""
    return predictive_percent  # Likelihood of preparation from 0 to 100%

# Assign weights to each factor
weights = {
    'difficulty': 0.15,
    'variety': 0.10,
    'healthiness': 0.25,
    'nutrient_balance': 0.10,
    'customization': 0.15,
    'satisfaction': 0.20,
    'time_cost_efficiency': 0.05,
    'predictive_performance': 0.10
}

# Function to calculate the overall score
def calculate_overall_score(scores, weights):
    overall_score = 0
    for metric, score in scores.items():
        weighted_score = score * weights.get(metric, 0)  # Multiply score by the weight for each factor
        overall_score += weighted_score
    return overall_score

# Example of input data (for one meal plan)
meal_plan_scores = {
    'difficulty': score_difficulty(3),  # Moderate difficulty
    'variety': score_variety(80),  # 80% variety
    'healthiness': score_healthiness(4),  # Healthy
    'nutrient_balance': score_nutrient_balance(90),  # Balanced nutrition
    'customization': score_customization(100),  # Perfect customization to user preferences
    'satisfaction': score_satisfaction(4),  # Very satisfied
    'time_cost_efficiency': score_time_cost_efficiency(75),  # 75% efficient
    'predictive_performance': score_predictive_performance(85)  # Likely to be prepared
}

# Calculate the overall score for this meal plan
overall_score = calculate_overall_score(meal_plan_scores, weights)

# Print the result
print(f"Overall Effectiveness Score: {overall_score:.2f}")


def score_meal_plan(meal_plan):
    # Implement your scoring logic here
    # For example, you can score based on nutritional balance, variety, etc.
    score = 0
    
    # Example scoring criteria
    if meal_plan['total macros'][0]['protein'] >= 130:
        score += 10
    if meal_plan['total macros'][1]['protein'] >= 100:
        score += 10
    if meal_plan['total macros'][0]['fiber'] >= 40:
        score += 5
    if meal_plan['total macros'][1]['fiber'] >= 30:
        score += 5
    
    # Add more scoring criteria as needed
    
    return score

def rate_models():
    meal_plans = retrieve_meal_plans()
    model_scores = {}
    
    for meal_plan in meal_plans:
        model = meal_plan['model']
        score = score_meal_plan(meal_plan)
        
        if model not in model_scores:
            model_scores[model] = []
        
        model_scores[model].append(score)
    
    # Calculate average score for each model
    for model, scores in model_scores.items():
        average_score = sum(scores) / len(scores)
        print(f"Model: {model}, Average Score: {average_score}")

if __name__ == "__main__":
    rate_models()