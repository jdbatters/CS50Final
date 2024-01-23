import requests
import json
import numbers
import requests
import random
from flask import redirect, session
from functools import wraps

def generate_recipes(ingredient):
    
    app_id = "ea4151cd"
    app_key = "1ff5cb51e0560cdc415cc1ef6f13ef91"
    url = ( f"https://api.edamam.com/api/recipes/v2?type=public&q="  
        +   f"{ingredient}" + 
            f"&app_id=" + app_id + "&app_key=" + app_key + "&imageSize=REGULAR"
    )
    response = requests.get(url)
    json = response.json()
    recipe_dict = {}
    all_recipes_list = []
    recipe_data_list = []
    recipe_generation_limit = range(5)
    api_generation_limit = json["to"]
    api_query_limit = list(range(0, api_generation_limit))
    random_int_list = random.sample(api_query_limit, 5)
    recipe_url_list = []
    
    for int in random_int_list:
        food_link = json["hits"][int]["recipe"]["url"]
        recipe_url_list.append(food_link)

    for item in recipe_generation_limit:
        random_value = random_int_list[item]
        individual_recipe_list = []
        food_label = json["hits"][random_value]["recipe"]["label"]
        food_image = json["hits"][random_value]["recipe"]["images"]["REGULAR"]["url"]
        food_ingredients = json["hits"][random_value]["recipe"]["ingredientLines"]
        food_source = json["hits"][random_value]["recipe"]["source"]
        
        individual_recipe_list.append([food_image, food_ingredients, food_label, food_source])
        all_recipes_list.append(individual_recipe_list)
    recipe_data_list.append((all_recipes_list, recipe_url_list))
        
    recipe_dict[ingredient] = recipe_data_list
    
    
    
    return(recipe_dict)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def check_for_nums(input):
    input_string = input.split()
    input = ''.join(str(i) for i in input_string)
    if input.isalpha() == True:
        return True
    else:
        return False

check_for_nums("sour cream2")
