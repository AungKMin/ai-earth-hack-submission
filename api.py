from openai import OpenAI
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
            "description": "item and a short descripton in parantheses for how to get the item sustainably",
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
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are chef who is also an expert in sustainability and recycling. You are skilled in giving a receipe for a meal with sustainable and recycled ingredients. You always return the ingredients and recipe instructions in JSON with no additonal description or context."}, 
            {"role": "user", "content": f"{prompt} Please provide a recipe with instructions and an ingredients list, with an emphasis on zero-waste and sustainable products. Do not label order numbers in instructions and ingredients."}
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


def imageURL(food):

    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model="dall-e-2",
        prompt=food,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url