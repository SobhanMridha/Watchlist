import os
from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, session
from flask_session import Session
import requests


load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&page=1"
    res = requests.get(url)
    data = res.json()
   
    return render_template("index.html", data=data)


