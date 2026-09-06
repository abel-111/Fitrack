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
- **Weight logging** — log weight over time, view history in a table, and see progress on a hand-drawn SVG line chart (no external chart library)
- **Community leaderboard** — top 20 users ranked by check-ins this month, with the logged-in user highlighted
- **Profile pictures** — upload a photo with an in-browser square crop step (Cropper.js) before saving
- **Avatar dropdown** — circular avatar in the navbar (photo or initial) opens a menu with Profile, Leaderboard, and Logout

## Database Models

- **User** — profile info, credentials, fitness level, goal, profile picture filename
- **Attendance** — one row per gym check-in, powers streaks and the leaderboard
- **WeightLog** — weight history over time, powers the progress chart
- **PreferredDay** — user's chosen workout days of the week (model exists, not yet surfaced in the UI)

## Project Structure
```
app/
    routes/
        auth.py           # signup, login, logout, dashboard
        attendance.py      # daily check-in
        weight.py          # weight logging + progress chart
        leaderboard.py      # monthly check-in leaderboard
        profile.py          # profile picture upload
    templates/
        base.html           # layout + avatar dropdown nav
        dashboard.html
        login.html
        signup.html
        weight.html
        leaderboard.html
        profile.html         # includes crop-before-upload UI
    static/
        css/style.css
        uploads/              # user-uploaded profile pictures (gitignored)
    models.py                # User, Attendance, WeightLog, PreferredDay + streak logic
    __init__.py               # app factory, blueprint registration
config.py
run.py
```

## Roadmap

- [x] Auth + user profiles
- [x] Attendance check-in + streaks
- [x] Weight log + progress chart
- [x] Community leaderboard
- [x] Profile picture upload with crop
- [ ] Preferred workout days in the UI
- [ ] Edit/delete weight log entries
- [ ] Deploy live (Render)

## Author

Abel — CS student, building this as a portfolio project alongside a Flask-based Expense Tracker.
