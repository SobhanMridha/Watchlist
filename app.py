import os
import sqlite3
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









@app.route('/')
def index():
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
    res = requests.get(url)
    data = res.json()
   
    return render_template("index.html", data=data)

@app.route("/watchlist", methods=["GET", "POST"])
def watchlist():
  
    return render_template("watchlist.html")

@app.route("/watched", methods=["GET", "POST"])
def watched():
   

    return render_template("watched.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            flash("Logged in successfully!", "success")
            return redirect("/")
        else:
            flash("Please enter both username and password.", "error")

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
        print(username, password, confirm_password)
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect("/register")
        if username and password:
            flash("Registered successfully!", "success")
            return redirect("/")
        else:
            flash("Please enter both username and password.", "error")

    return render_template("register.html")


 