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

    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(weight_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(workouts_bp)
    app.register_blueprint(diet_bp)
    app.register_blueprint(ai_bp)

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
                conn.commit()
        except Exception as e:
            app.logger.warning(f"Schema upgrade notice: {e}")

    return app