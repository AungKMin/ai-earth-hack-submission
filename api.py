from openai import OpenAI
import os
from dotenv import dotenv_values
import json

api_key = dotenv_values(".env")['CHATGPTKEY']

# api_string_response = '{"dish": "Pancake", "ingredients": ["Flour", "Plant-based milk", "Vegan egg substitute", "Maple syrup", "Sustainably sourced cooking oil"], "instructions": ["In a mixing bowl, combine flour and vegan egg substitute.", "Gradually add plant-based milk and stir until smooth.", "Heat a non-stick pan over medium heat and add a small amount of cooking oil.", "Pour a ladleful of batter into the pan and spread it evenly.", "Cook for about 2 minutes or until bubbles form on the surface.", "Flip the pancake and cook for another 1-2 minutes.", "Repeat with the remaining batter.", "Serve the pancakes warm with maple syrup."]}'
# api_json_response = json.loads(api_string_response)  

def get_json(dish):
    return gptPrompt(dish)

def gptPrompt(food):
    client = OpenAI(api_key=api_key)

    prompt = f"return a recipe for {food}"

    schema = {
        "type": "object",
        "properties": {
            "dish": {
            "type": "string",
            "description": "Descriptive title of the dish"
            },
            "ingredients": {
            "type": "array",
            "items": {"type": "string"}
            },
            "instructions": {
            "type": "array",
            "description": "Steps to prepare the recipe.",
            "items": {"type": "string"}
            }
        },
        "requried": ["ingredients", "instructions"]
        }

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert chef in sustainability, skilled in giving a receipe for a meal with sustainable ingredients. You always return just the JSON with no additonal description or context."}, 
            {"role": "user", "content": f"{prompt} Please do so in line with sustainability. Do not mention the quantity in ingredients"}
        ],
        functions=[
            {
                "name": "generate_code",
                "description": "generates code and description in JSON format. used by code assistants",
                "parameters": schema
            }
        ]
        )

    decoded_response = json.loads(response.choices[0].message.function_call.arguments.strip())

    return decoded_response