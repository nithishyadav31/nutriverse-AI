from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
import random
import numpy as np
import matplotlib.pyplot as plt
import base64

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)

# Nutritionix API Credentials
NUTRITIONIX_APP_ID = "dc78b0ed"
NUTRITIONIX_APP_KEY = "92375a867ab7d1ff36afdcc362b266e7"
NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

@app.route('/')
def home():s
    return "Flask server is running!"

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request body"}), 400

        # Sample 7-day meal plan with calories
        meal_plan = {
            "Sunday": {
                "breakfast": {"meal": "Oatmeal with fruits", "calories": 350},
                "lunch": {"meal": "Grilled chicken with salad", "calories": 600},
                "dinner": {"meal": "Steamed fish with vegetables", "calories": 500},
            },
            "Monday": {
                "breakfast": {"meal": "Scrambled eggs with toast", "calories": 400},
                "lunch": {"meal": "Quinoa salad with grilled tofu", "calories": 550},
                "dinner": {"meal": "Lentil soup with brown rice", "calories": 480},
            },
            "Tuesday": {
                "breakfast": {"meal": "Smoothie with nuts and seeds", "calories": 300},
                "lunch": {"meal": "Grilled salmon with veggies", "calories": 620},
                "dinner": {"meal": "Chickpea curry with naan", "calories": 530},
            },
            "Wednesday": {
                "breakfast": {"meal": "Greek yogurt with honey", "calories": 320},
                "lunch": {"meal": "Chicken stir-fry with brown rice", "calories": 650},
                "dinner": {"meal": "Baked tofu with quinoa", "calories": 510},
            },
            "Thursday": {
                "breakfast": {"meal": "Whole grain pancakes with peanut butter", "calories": 380},
                "lunch": {"meal": "Tuna sandwich with salad", "calories": 570},
                "dinner": {"meal": "Mixed vegetable soup with garlic bread", "calories": 450},
            },
            "Friday": {
                "breakfast": {"meal": "Boiled eggs with avocado toast", "calories": 390},
                "lunch": {"meal": "Beef stir-fry with rice", "calories": 630},
                "dinner": {"meal": "Pasta with veggies and olive oil", "calories": 540},
            },
            "Saturday": {
                "breakfast": {"meal": "Protein shake with banana", "calories": 310},
                "lunch": {"meal": "Baked chicken with brown rice", "calories": 600},
                "dinner": {"meal": "Steamed broccoli with grilled fish", "calories": 500},
            }
        }

        # Calculate total calories for each day
        for day, meals in meal_plan.items():
            total_calories = sum(meal["calories"] for meal in meals.values())
            meals["total_calories"] = total_calories

        return jsonify({"meal_plan": meal_plan})

    except Exception as e:
        logging.error(f"Error generating meal plan: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get-nutrition', methods=['POST'])
def get_nutrition():
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Invalid request body. Expected 'query' field."}), 400

        logging.info(f"Received nutrition query: {data['query']}")

        # Make a request to Nutritionix API
        headers = {
            "x-app-id": NUTRITIONIX_APP_ID,
            "x-app-key": NUTRITIONIX_APP_KEY,
            "Content-Type": "application/json"
        }
        payload = {"query": data["query"]}
        
        response = requests.post(NUTRITIONIX_API_URL, headers=headers, json=payload)
        
        # Debugging: Print full API response
        response_json = response.json()
        logging.info(f"Nutritionix API Response: {response_json}")

        # Check if the request was successful
        if response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch nutrition data",
                "details": response_json
            }), response.status_code

        # Check if the response contains valid food data
        if "foods" not in response_json or not response_json["foods"]:
            return jsonify({"error": "No nutritional data found for the given query."}), 404

        # Clean up nutrition data and format it as needed
        food_item = response_json["foods"][0]
        nutrition_data = {
            "food_name": food_item.get("food_name", ""),
            "nf_calories": food_item.get("nf_calories", 0),
            "nf_protein": food_item.get("nf_protein", 0),
            "nf_total_carbohydrate": food_item.get("nf_total_carbohydrate", 0),
            "nf_total_fat": food_item.get("nf_total_fat", 0),
        }

        return jsonify({"foods": [nutrition_data]})

    except Exception as e:
        logging.error(f"Error fetching nutrition data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
