from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from app.models import db, User

login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.attendance import attendance_bp
    from app.routes.weight import weight_bp
    from app.routes.leaderboard import leaderboard_bp
    from app.routes.profile import profile_bp
    from app.routes.workouts import workouts_bp
    from app.routes.diet import diet_bp
    from app.routes.ai import ai_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(weight_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(workouts_bp)
    app.register_blueprint(diet_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        # Safe SQLite schema migration for newly added User fields
        try:
            from sqlalchemy import text
            with db.engine.connect() as conn:
                cols_result = conn.execute(text("PRAGMA table_info(user)")).fetchall()
                col_names = [col[1] for col in cols_result]

                if 'role' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(50) DEFAULT 'general'"))
                if 'dietary_preference' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN dietary_preference VARCHAR(30) DEFAULT 'standard'"))
                if 'activity_level' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN activity_level VARCHAR(30) DEFAULT 'moderate'"))
                if 'is_coach' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN is_coach BOOLEAN DEFAULT 0"))
                if 'coach_bio' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN coach_bio VARCHAR(300) DEFAULT 'Certified Fitness & Nutrition Specialist'"))
                if 'coach_specialty' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN coach_specialty VARCHAR(100) DEFAULT 'General Fitness, Strength & Nutrition'"))
                # New fields
                if 'coach_approved' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN coach_approved BOOLEAN DEFAULT 0"))
                if 'is_admin' not in col_names:
                    conn.execute(text("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
                conn.commit()

            # Seed default admin if none exists
            if not User.query.filter_by(is_admin=True).first():
                admin = User(
                    username="admin",
                    email="admin@fitrack.com",
                    is_admin=True,
                    is_coach=False,
                    role="general"
                )
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()

            # Seed default certified coaches if none exist (auto-approved)
            if not User.query.filter_by(is_coach=True).first():
                coach1 = User(
                    username="coach_raghav",
                    email="coach.raghav@fitrack.com",
                    is_coach=True,
                    coach_approved=True,
                    coach_bio="Senior Strength & Bodybuilding Coach with 10+ years helping clients master progressive overload, muscle recovery, and nutrition.",
                    coach_specialty="Progressive Overload & Strength Coaching",
                    role="bodybuilder"
                )
                coach1.set_password("coach123")

                coach2 = User(
                    username="coach_ananya",
                    email="coach.ananya@fitrack.com",
                    is_coach=True,
                    coach_approved=True,
                    coach_bio="Holistic Nutritionist & Fat Loss Specialist focused on clean, high-protein home meal planning and sustainable habits.",
                    coach_specialty="Nutrition Planning & Fat Loss",
                    role="athlete"
                )
                coach2.set_password("coach123")

                db.session.add_all([coach1, coach2])
                db.session.commit()

            # Ensure existing coaches from old seed (without coach_approved set) get approved
            from sqlalchemy import text as _text
            with db.engine.connect() as conn:
                conn.execute(_text(
                    "UPDATE user SET coach_approved = 1 WHERE is_coach = 1 AND (coach_approved IS NULL OR coach_approved = 0) "
                    "AND email LIKE '%fitrack.com'"
                ))
                conn.commit()

        except Exception as e:
            app.logger.warning(f"Schema upgrade notice: {e}")

    return app