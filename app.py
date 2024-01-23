from flask import Flask, flash, redirect, render_template, request, session, flash
from flask_session import Session
from helpers import login_required, generate_recipes, check_for_nums
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


connect = sqlite3.connect('pantry.db', check_same_thread=False)
connect.execute('CREATE TABLE IF NOT EXISTS pantry (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, available_food TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))')
connect.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, pw_hash TEXT NOT NULL)')
connect.close()


@app.route("/")
@login_required
def index():
    pantry_list = []
    
    connect = sqlite3.connect('pantry.db', check_same_thread=False) 
    pantry = connect.execute("SELECT available_food FROM pantry WHERE user_id = ?", (session["user_id"],)).fetchall()
    
    card_data = {}
    for i in range(len(pantry)):
        pantry_list.append(pantry[i][0])
    if not pantry_list:
        empty_pantry = True
    else:
        empty_pantry = False
    print(empty_pantry)
    for ingredient in pantry_list:
        recipe_dict = generate_recipes(ingredient)
        card_data[ingredient] = recipe_dict
    total_cards = [*range(3)]
    


    return render_template("index.html", recipe_info=card_data, pantry_list=pantry_list, total_cards=total_cards, empty_pantry=empty_pantry )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        session.clear()
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username", 'error')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", 'error')
            return render_template("login.html")

        # Query database for username
        connect = sqlite3.connect('pantry.db', check_same_thread=False)
        rows = connect.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        connect.close()
        password = request.form.get("password")
        
        # if query produces empty list then username is incorrect
        if len(rows) != 0:
            pw_hash = rows[0][2]
        else:
            flash("Invalid username", 'error')
            return render_template("login.html")

        # Ensure password is correct
        if not check_password_hash(pw_hash, password):
            flash("Invalid password", 'error')
            return render_template("login.html")
        
        session["user_id"] = rows[0][1]
        return redirect("/")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/pantry", methods=["GET", "POST"])
@login_required
def pantry():
    if request.method == "GET":

        connect = sqlite3.connect('pantry.db', check_same_thread=False) 
        pantry = connect.execute("SELECT available_food FROM pantry WHERE user_id = ?", (session["user_id"],)).fetchall()
        pantry_list = []

        for i in range(len(pantry)):
            pantry_list.append(pantry[i][0])
        return render_template("pantry.html", pantry=pantry_list)
    
    else:
        food_item = request.form.get("food").title()


        if len(food_item) < 3:
            flash('Food must be spelled with at least 3 letters', 'error')
            return redirect("/pantry")
        elif check_for_nums(food_item) == False:
            flash('Food cannot contain numbers', 'error')
            return redirect("/pantry")
        else:
            with sqlite3.connect('pantry.db', check_same_thread=False) as pantry:
                cursor = pantry.cursor()
                cursor.execute("INSERT INTO pantry (available_food, user_id) VALUES (?, ?)", (food_item, session["user_id"]))
                pantry.commit()
                cursor.close()
            flash('Your pantry has been updated', 'success')
            return redirect("/pantry")

@app.route("/pantry_delete", methods=["POST"])
def pantry_delete():
    food_item = request.form.to_dict()
    food_item = list(food_item.keys())[0]
    with sqlite3.connect('pantry.db', check_same_thread=False) as pantry:
        cursor = pantry.cursor()
        cursor.execute("DELETE FROM pantry WHERE available_food = ? AND user_id = ?", (food_item, session["user_id"]))
        pantry.commit()
        cursor.close()
        food_item = str(food_item)
        flash(food_item + ' has been removed from your pantry!', 'success')
        return redirect("/pantry")
    

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")
    
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("confirmation")
        connect = sqlite3.connect('pantry.db', check_same_thread=False) 
        existing_user = connect.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        
        if len(existing_user) != 0:
            flash("Username already exists!", 'error')
            return render_template("register.html")
        elif not username or not password or not password_confirm:
            flash("Please fill in all fields", 'error')
            return render_template("register.html")
        elif len(username) < 3:
            flash('Username must be longer than 2 characters', 'error')
            return render_template("register.html")
        elif len(password) < 5:
            flash('Password must be at least 5 characters', 'error')
            return render_template("register.html")
        elif password != password_confirm:
            flash('Passwords do not match', 'error')
            return render_template("register.html")
        else:
            if password == password_confirm:
                pw_hash = generate_password_hash(password)
                with sqlite3.connect('pantry.db', check_same_thread=False) as users:
                    cursor = users.cursor()
                    cursor.execute("INSERT INTO users (username, pw_hash) VALUES(?, ?)", (username, pw_hash))
                    users.commit()
                    cursor.close()
                    flash('Account successfully created!', 'success')
            else:
                flash("Password fields must match", category='error')
                return render_template("register.html")
        return redirect("/")




