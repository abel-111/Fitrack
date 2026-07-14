# Fitrack
Track your reps, your meals, and your macros — all in one place.
the fun is going to begin now## Setup

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

## Database Models

- **User** — profile info, credentials, fitness level, goal
- **Attendance** — one row per gym check-in, powers ranking/streaks
- **WeightLog** — weight history over time, for progress charts
- **PreferredDay** — user's chosen workout days of the week

## Author

Abel — CS student, building this as a portfolio project alongside an Flask-based Expense Tracker.