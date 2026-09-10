# Fitrack — AI-Powered Fitness & Nutrition Platform

Track your reps, your meals, and your macros — with an intelligent role-aware AI Coach tailored to your lifestyle.

---

## Setup & Running

```bash
# Clone the repo
git clone <repo-url>
cd Fitrack

# Install dependencies
pip install -r requirements.txt

# Run the app (database tables and schema migrations auto-initialize on startup)
python run.py
```

Visit `http://127.0.0.1:5000` in your browser.

*(Optional)* To enable live external Gemini generative AI model responses, set `GEMINI_API_KEY` in your environment or `.env` file. Even without a key, Fitrack includes a built-in expert nutrition and fitness coach engine.

---

## Features

### 🥗 AI Diet & Nutrition Blueprint
- **Role-Aware Personalization**: Generates 4-meal daily meal plans (Breakfast, Lunch, Pre/Post-workout Snack, Dinner) tailored specifically to your daily persona:
  - 💼 **Desk Worker / Corporate**: Low-glycemic lunches to avoid the 2 PM food coma, high fiber, desk snack suggestions.
  - 🎓 **Student**: Budget-friendly meal prep (eggs, oats, lentils, peanut butter), high energy for study sessions.
  - 🏃 **Athlete**: Carb loading and rapid glycogen re-synthesis around training windows.
  - 🏋️ **Bodybuilder**: Leucine-threshold optimized protein feedings (30g+ per meal), progressive overload macros.
  - 👨‍👩‍👧 **Busy Parent / Pro**: Fast, one-pan family-friendly sheet meals.
  - 🧘 **General Fitness**: 80/20 balanced longevity nutrition.
- **Dietary Preferences**: Supports Standard / Balanced, Vegetarian, 100% Vegan, and Keto / Low-Carb.
- **Precision Macros & TDEE**: Automatic Mifflin-St Jeor BMR, Activity-adjusted TDEE, and exact protein/carb/fat targets.
- **Interactive Daily Adherence**: Mark meals eaten throughout the day to track your consistency percentage.

### 🤖 FitBot Interactive AI Coach
- **Floating AI Assistant**: Accessible from any page via the floating AI button.
- **Role-Specific Context**: Understands your current weight, goal (cutting/bulking/maintaining), streak, and role.
- **Quick-Prompt Chips**: Instant answers for macros, desk posture routines, pre-workout snacks, and plateau troubleshooting.

### ✨ AI Coaching Diagnostics & Recommendations
- **Consistency Score**: 0-100% rating based on streak momentum and check-in frequency.
- **Weight Trajectory Analysis**: Intelligent forecasting comparing current progress with target weight.
- **Role Mobility Warm-Up**: 5-minute pre-workout mobility sequence (e.g. Desk Posture Reset, Dynamic Elasticity Primer).
- **Evidence-Based Supplement Stack**: Curated dosages and science-backed benefits for your fitness goal.

### 🏋️ Training & Community
- **Workout Splits**: Level-tailored routines (Beginner, Intermediate, Advanced) with technique cues, rest timers, and interactive set tracking checkboxes.
- **Weight Logging**: Track history with an interactive SVG progress chart and real-time BMI diagnostics.
- **Community Leaderboard**: Monthly check-in rankings with gold 🥇, silver 🥈, and bronze 🥉 podium badges.
- **Profile & Avatar Cropper**: Upload profile picture with in-browser square cropping (Cropper.js) and configure comprehensive biometrics.

---

## Database Models

- **User**: Authentication, credentials, role (`desk_worker`, `student`, `athlete`, `bodybuilder`, `busy_parent`, `general`), dietary preference, activity level, fitness level, goal, height, weight, target weight, age, gender.
- **UserDietPlan**: Active and historical AI meal plans, macro targets, role benefits, and meal completion state.
- **Attendance**: Daily gym check-ins, powering streaks and community leaderboards.
- **WeightLog**: Historical weight tracking with progress curve points.
- **PreferredDay**: User's chosen workout schedule across the week.

---

## Project Structure

```
app/
    routes/
        auth.py           # signup, login, logout, dashboard
        diet.py           # AI diet plans, generation, meal checkoffs
        ai.py             # AI coach chat, diagnostics & recommendations
        attendance.py      # daily gym check-in
        weight.py          # weight logging + progress chart
        leaderboard.py      # monthly check-in leaderboard
        profile.py          # biometrics, lifestyle role, and avatar crop
        workouts.py        # workout splits & role mobility warmups
    services/
        ai_coach.py        # TDEE/macro algorithms, recipe catalog, AI coach engine
    templates/
        base.html           # layout, navigation, and floating AI Coach widget
        dashboard.html     # AI daily focus, streak flame, metrics, quick hub
        diet.html          # AI meal blueprint, macro meters, adherence checklist
        recommendations.html # AI coaching diagnostics, supplement stack
        workouts.html      # exercise split with role mobility & set trackers
        weight.html        # weight history & SVG progress chart
        leaderboard.html   # community podium rankings
        profile.html       # biometrics, role selector, BMI/TDEE calculation
        login.html         # login page
        signup.html        # signup with role selection
    static/
        css/style.css      # modern obsidian & energetic coral dark design system
        uploads/           # cropped user profile avatars
    models.py             # User, UserDietPlan, Attendance, WeightLog, PreferredDay
    __init__.py            # app factory, blueprint registration & auto-migration
config.py
run.py
requirements.txt
```
