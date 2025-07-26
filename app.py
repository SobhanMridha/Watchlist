import os
import sqlite3
import json
from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
DATABASE = "database.db"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # optional: access columns by name
    return g.db


def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

with open("genres.json") as file:
    genres = json.load(file)






@app.route('/')
def index():
    title = request.args.get('title', '').strip()
    selected_category = request.args.get('category')
    data = None

    if title:
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': API_KEY,
            'language': 'en-US',
            'query': title,
            'page': 1,
            'include_adult': False
        }
        res = requests.get(url, params=params)
        data = res.json()

    elif selected_category:
        url = f"https://api.themoviedb.org/3/movie/{selected_category}"
        params = {
            'api_key': API_KEY,
            'language': 'en-US',
            'page': 1
        }
        res = requests.get(url, params=params)
        data = res.json()
    else:
        url = "https://api.themoviedb.org/3/movie/now_playing"
        params = {
            'api_key': API_KEY,
            'language': 'en-US',
            'page': 1
        }
        res = requests.get(url, params=params)
        data = res.json()

    return render_template("index.html", data=data, selected_category=selected_category, genres=genres)


@app.route("/watchlist", methods=["GET", "POST"])
def watchlist():
    if not session.get("user_id"):
        flash("You must be logged in to view this page.", "error")
        return redirect("/login")

    return render_template("watchlist.html")

@app.route("/watched", methods=["GET", "POST"])
def watched():
    if not session.get("user_id"):
        flash("You must be logged in to view this page.", "error")
        return redirect("/login")

    return render_template("watched.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return redirect("/login")
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        print(user)
        if user and check_password_hash(user["password_hash"], password):
            
            session["user_id"] = user["id"]
            flash("Logged in successfully!", "success")
            return redirect("/")
        else:
            flash("Invalid username or password.", "error")
            return redirect("/login")
    

    return render_template("login.html")



@app.route("/logout")
def logout():
    
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
    
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect("/register")
        if username and password:
            hash = generate_password_hash(password)
            try:
                db = get_db()
                db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash))
                db.commit()
            except:
                flash("Username already exists.", "error")
                return redirect("/register")

            flash("Registered successfully!", "success")
            return redirect("/login")
        else:
            flash("Please enter both username and password.", "error")
            return redirect("/register")

    return render_template("register.html")


 