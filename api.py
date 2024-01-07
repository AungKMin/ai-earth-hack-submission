import json

api_string_response = '{"dish": "Pancake", "ingredients": ["Flour", "Plant-based milk", "Vegan egg substitute", "Maple syrup", "Sustainably sourced cooking oil"], "instructions": ["In a mixing bowl, combine flour and vegan egg substitute.", "Gradually add plant-based milk and stir until smooth.", "Heat a non-stick pan over medium heat and add a small amount of cooking oil.", "Pour a ladleful of batter into the pan and spread it evenly.", "Cook for about 2 minutes or until bubbles form on the surface.", "Flip the pancake and cook for another 1-2 minutes.", "Repeat with the remaining batter.", "Serve the pancakes warm with maple syrup."]}'
api_json_response = json.loads(api_string_response)  

def get_json(dish):
    return api_json_response