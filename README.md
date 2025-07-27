
# Watchlist

#### Video Demo:  <https://www.youtube.com/watch?v=jUdN1-30Pcs>

#### Description:

# 🎬 Watchlist - Movie Watchlist & Watched Tracker

**Watchlist** is a Flask web application that empowers users to discover new movies, create a personalized watchlist, and track what they’ve already watched. Leveraging the TMDb API, it displays real-time movie data—posters, ratings, genres, release dates—and provides a responsive interface built with Tailwind CSS. This README documents every component of the project, explains the rationale behind key design choices, and guides you through setup, usage, and deployment.

---

## 📂 File Structure & Responsibilities

```
watchlist/
├── app.py
├── database.db
├── genres.json
├── requirements.txt
├── Procfile
├── .gitignore
├── static/
│   ├── css/
│   └── images/
└── templates/
    ├── layout.html
    ├── index.html
    ├── watchlist.html
    ├── watched.html
    └── login.html / register.html
```

**app.py**  
This is the heart of the application. It defines all Flask routes and business logic:  
- `/` handles search, category filtering (popular, top_rated, now_playing, upcoming), and renders the homepage.  
- `/watchlist` and `/watched` (POST) insert movie IDs into the SQLite tables.  
- `/remove` and `/move` manage deletion and migration between watchlist and watched lists.  
- Database setup uses `get_db()` for SQLite3 connections and enforces unique constraints on `(user_id, movie_id)`.

**database.db**  
A SQLite database storing two tables—`watchlist` and `watched`—alongside a `users` table . Unique constraints on `(user_id, movie_id)` prevent duplicates.

**genres.json**  
A static JSON mapping TMDb genre IDs to names. We chose this to avoid repeated API calls for genre lists, speeding up template rendering and limiting TMDb rate usage.

**requirements.txt**  
Contains all Python dependencies, including `Flask`, `gunicorn`, `requests`, and `itsdangerous`. Keep this updated via `pip freeze > requirements.txt`.

**Procfile**  
Used by Render for deployment:
```
web: gunicorn app:app
```
Specifies that `gunicorn` should serve the `app` object from `app.py`.

**.gitignore**  
Excludes `__pycache__/`, environment files, and any local secrets. Note: we do **not** ignore `database.db` for the demo, so initial data ships with the repo.

**static/**  
- **css/**: Custom CSS overrides (if any) alongside Tailwind defaults.  
- **images/**: Hero background and any locally stored assets.

**templates/**  
- **layout.html**: Base template defining head, navigation, and flash message blocks. Includes Tailwind imports.  
- **index.html**: Extends `layout.html`, defines the hero section, search/category bar, and main content area. It also includes the movie grid and handles search and filter functionality (via form submissions).

- **watched.html**: Renders a grid similar to the homepage but for movies fetched by ID from the `watched` table.  
- **watchlist.html**: Renders a grid similar to the homepage but for movies fetched by ID from the `watchlist` table.
- **login.html / register.html**: For user authentication.

---

## ⚙️ Setup & Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/watchlist.git
   cd watchlist
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Obtain TMDb API key**  
   - Sign up at [TMDb](https://www.themoviedb.org).  
   - In `app.py`, set:  
     ```python
     API_KEY = "your_tmdb_api_key"
     app.secret_key = "a_random_secret_key"
     ```  
   - Or export as environment variables.

5. **Initialize the database**  
   If you wish to start fresh or migrate:  
   ```bash
   flask shell
   >>> from app import init_db
   >>> init_db()  # creates tables
   ```

6. **Run Locally**  
   ```bash
   flask run
   ```  
   Visit `http://127.0.0.1:5000/`.

---

## 🚀 Deployment to Render

1. **Push to GitHub**, linking your repo to Render.  
2. **Create New Web Service** on Render.com:  
   - Environment: Python 3  
   - Build Command: `pip install -r requirements.txt`  
   - Start Command: `gunicorn app:app`  
3. **Ensure** `database.db` is tracked if you want initial data. For real-world apps, switch to PostgreSQL via Render’s managed databases.

---

#### Thank you for exploring **Watchlist**! Feel free to fork, contribute, or adapt this project.  
#### Made with ❤️ by Sobhan Mridha as part of the CS50x final project.







