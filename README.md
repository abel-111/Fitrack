# Fitrack — AI-Powered Fitness & Nutrition Platform

Track your reps, your meals, and your macros — with an intelligent role-aware AI Coach, strict Push/Pull/Legs (PPL) workout splits, and seamless Light/Dark mode styling tailored to your lifestyle.

---

## ⚡ Setup & Running

```bash
# Clone the repository
git clone https://github.com/abel-111/Fitrack.git
cd Fitrack

# Install dependencies
pip install -r requirements.txt

# Run the app (database tables and migrations initialize automatically on startup)
python run.py
```

Visit `http://127.0.0.1:5000` in your browser.

*(Optional)* To enable live external Gemini generative AI model responses, set `GEMINI_API_KEY` in your environment or `.env` file. Even without an API key, Fitrack has a built-in expert nutrition, workout overload, and coaching engine.

---

## 🌟 Key Features

### 🏋️ Pure Push-Pull-Legs (PPL) Splits & Overload Tracking
- **Strict PPL Split**: No push and pull exercises are ever mixed in a single training day, ensuring optimal recovery and muscle group isolation.
- **Level-Tailored Programming**:
  - **Beginner (3-Day PPL)**: Foundation Chest/Shoulders/Triceps (Push), Back/Lats/Biceps (Pull), Quads/Hamstrings/Calves/Abs (Legs).
  - **Intermediate (4-Day PPL + Legs & Shoulders)**: Push Hypertrophy, Pull Hypertrophy, Legs & Core Power, and a dedicated **Legs & Shoulders** day.
  - **Advanced (6-Day PPL Hypertrophy & Detail)**: Heavy Push, Density Pull, Heavy Legs/Abs, Weak-Point Push, Detail Pull, and a dedicated **Legs & Shoulders Complete** day.
- **Daily Workout Tracker**: Log exercises, working sets, reps, weight, volume load, and automatic progressive overload target calculations.
- **Warm-Up Sequences**: 5-minute pre-workout routines tailored to your lifestyle (e.g. Desk Posture Reset, Elasticity Primer).

### 🌓 Telegram-Style Light & Dark Theme
- **Smooth Circular Transition**: Telegram-style circular view transitions and ripple animations when toggling themes.
- **Optimized Dark Mode Contrast**: Curated color palette (`#0f0d19` background with high-contrast text and luminous badges) ensuring all typography, macro breakdown pills, meal cards, input fields, and tables remain crisp and legible in dark mode.

### 🥗 AI Diet & Nutrition Blueprint
- **Role-Aware Personalization**: Generates 4-meal daily meal plans (Breakfast, Lunch, Pre/Post-workout Snack, Dinner) tailored specifically to your daily persona:
  - 💼 **Desk Worker / Corporate**: Low-glycemic meals avoiding afternoon energy crashes, high fiber, desk snack suggestions.
  - 🎓 **Student**: Budget-friendly meal prep (eggs, oats, lentils, peanut butter), high energy for study sessions.
  - 🏃 **Athlete**: Carb loading and rapid glycogen re-synthesis around training windows.
  - 🏋️ **Bodybuilder**: Leucine-threshold optimized protein feedings (30g+ per meal), progressive overload macros.
  - 👨‍👩‍👧 **Busy Parent / Pro**: Fast, one-pan family-friendly sheet meals.
  - 🧘 **General Fitness**: 80/20 balanced longevity nutrition.
- **South Indian Regional Cuisines**: Authentic dietary preferences spanning Tamil Nadu, Kerala, Karnataka, Andhra/Telangana, and Continental/Healthy Fusion options.
- **Daily Food Log & Macro Counter**: Search common food database, add servings with quick steppers, calculate real-time macros, and log food entries.

### 🤖 FitBot Interactive AI Coach & Coaching Diagnostics
- **Floating AI Coach**: Accessible from any page via the floating assistant widget.
- **Context-Aware Recommendations**: Tailored answers considering current weight, target weight, goal (cutting/bulking/maintaining), streak, and role.
- **Coaching Diagnostics**: Consistency Score (0-100%), weight trajectory insights, role hydration targets, and science-backed supplement protocol.

### 🏆 Community & Administrative Portal
- **Community Leaderboard**: Monthly check-in rankings with podium medals 🥇 🥈 🥉 and user streak counters.
- **Coach Portal**: Certified coaches can review client inquiries, review client profiles, and send tailored guidance.
- **Master Admin Center**: Superadmin management over clients, certified coaches, applications, and accounts.

---

## 🗄️ Database Models

- **User**: Authentication, credentials, role, dietary preference, activity level, fitness level, goal, weight, target weight, biometrics, coach status, and avatar storage.
- **WorkoutLog**: Daily workout logs, exercises, sets, reps, volume, units, and progressive overload targets.
- **FoodLog**: Daily logged food entries, meal slots (Breakfast, Lunch, Snacks, Dinner), calories, and macronutrients.
- **UserDietPlan**: Active and historical AI meal plans, macro targets, role benefits, and meal completion states.
- **Attendance**: Daily gym check-ins powering active streaks and community leaderboard rankings.
- **WeightLog**: Historical weight tracking with progress curve points.
- **ChatMessage**: Client and coach communication threads.

---

## 📁 Project Structure

```
app/
    routes/
        admin.py          # Master admin control center and coach approvals
        ai.py             # AI coach chat, diagnostics & coach inbox
        attendance.py     # Daily gym check-in
        auth.py           # Signup, login, logout, dashboard
        diet.py           # AI diet plans, generation, food tracking
        leaderboard.py    # Monthly check-in leaderboard
        profile.py        # Biometrics, lifestyle role, and avatar cropping
        weight.py         # Weight logging + progress chart
        workouts.py       # Strict PPL workout splits & workout logger
    services/
        ai_coach.py       # TDEE/macro algorithms, recipe catalog, AI coach engine
        food_database.py  # Preset food items and macro reference
        workout_database.py # Preset exercise catalog & muscle group tagging
    templates/
        admin_portal.html # Superadmin control center
        base.html         # Base layout, theme toggle & floating AI Coach widget
        dashboard.html    # Quick hub, daily overview, active streaks
        diet.html         # AI meal blueprint, food tracker & macro counter
        leaderboard.html  # Community podium rankings
        login.html        # Authentication login page
        profile.html      # Biometrics, role selector, BMI/TDEE calculations
        recommendations.html # AI coaching diagnostics, supplement protocol
        signup.html       # Account registration with role selection
        weight.html       # Weight history & SVG progress chart
        workouts.html     # PPL workout routine, daily workout logger
    static/
        css/style.css     # Light purple & obsidian dark design system
        uploads/          # Cropped user profile avatars
    models.py             # SQLAlchemy models
    __init__.py           # App factory, blueprints & migrations
config.py
run.py
test_food_tracker.py
test_workout_tracker.py
requirements.txt
```

---

## 🧪 Testing

Run the automated test suite with Python's built-in `unittest`:

```bash
python -m unittest discover
```
