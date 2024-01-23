# Recipe Generator using Edamam Api

## A web application using Flask to generate random recipe inspiration for my CS50x final project

### Video Demo: <>

## Tech Used

1: Python (Flask)
2: HTML, CSS, Bootstrap
3: SQLite

## Description

This is my final project for Harvard's CS50 Introduction to Computer Science. It is a web application that generates recipes pulled from the Edamam Recipe Search V2 API based on user inputs. The intention of this project was to reduce the friction of cooking at home. Removing the difficulty of deciding what to make will hopefully make cooking at home more likely.

## Installation

pip3 install -r requirements.txt

### Main Files

1.  app.py - The flask backend with routes for each web page.
2.  helpers.py - Functions for the API call, login decorator, and validating user inputs.
3.  static & templates - CSS and HTML for the web app.
4.  pantry.db - Simple database for storing user login and "pantry" data.

### Using the application

1. Run the program with flask run in the terminal to host the webpage on a local server.
2. Users must create an account in order to use the application.
3. After logging in, users can fill their virtual pantry to reflect the food they have available at home, or delete any food.
4. The homepage will populate with 3 recipe cards per item with a picture, recipe name, required ingredients and a link to the recipe source webpage.

### Customizing output

To change the number of recipes pulled from JSON data change the value of num_of_recipes in the generate_recipes function in helpers.py. The number of cards per pantry item can also be changed from its current value of 3 by changing the value of total_cards, however the value of total_cards should be less than or equal to the value of num_of_recipes.

### Database

pantry.db is a simple relational database using SQL. There are only 2 tables contained within, users - to store login information of users, and pantry - to store food data of each user.

### Features to add

While I am very happy with the state of this application, I do have some improvements I would like to add in future iterations.

1. Include options to filter results by:
   - Cuisine type
   - Number of ingredients
   - Time to prepare
   - Including/excluding certain ingredients
2. Allow users to change the number of cards generated
3. Add a larger variety of recipes generated
   - The app is currently limited to the first page of the JSON data, leaving only 20 recipes per item to be selected. Accessing the paginated data increases the already sluggish loading times to an unnacceptable length.
