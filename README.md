# Fitrack
Track your reps, your meals, and your macros — all in one place.

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd Fitrack

# Install dependencies
pip install -r requirements.txt

# Create the database
python
>>> from app import create_app
>>> from app.models import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()

# Run the app
python run.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Features

- **Auth** — signup, login, logout with hashed passwords (Flask-Login)
- **Dashboard** — shows fitness level, goal, and attendance stats at a glance
- **Attendance check-in** — one-click daily check-in; a user can only check in once per day
- **Streak tracking** — current streak, longest streak, and this month's check-in count, computed live from attendance history

## Database Models

- **User** — profile info, credentials, fitness level, goal
- **Attendance** — one row per gym check-in, powers streaks and (later) ranking
- **WeightLog** — weight history over time, for progress charts
- **PreferredDay** — user's chosen workout days of the week

## Project Structure