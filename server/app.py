# ═══════════════════════════════════════════════════════════
# server/app.py — Flask Application Factory
# ═══════════════════════════════════════════════════════════

import os
from flask import Flask
from server.extensions import db, jwt, bcrypt, cors

# Resolve paths at module load time (not inside create_app)
# _SERVER_DIR  = .../UPSA_CHATBOT/server/
# _PROJECT_ROOT = .../UPSA_CHATBOT/
# _CLIENT_DIR  = .../UPSA_CHATBOT/client/
_SERVER_DIR   = os.path.abspath(os.path.dirname(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SERVER_DIR, ".."))
_CLIENT_DIR   = os.path.join(_PROJECT_ROOT, "client")


def create_app():
    app = Flask(
        __name__,
        static_folder=_CLIENT_DIR,
        static_url_path=""
    )

    # ── Load .env if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # ── Configuration
    app.config["SECRET_KEY"]                     = os.environ.get("SECRET_KEY", "upsa-itm-secret-change-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"]        = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(_PROJECT_ROOT, 'upsa_itm.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"]                 = os.environ.get("JWT_SECRET_KEY", "upsa-jwt-secret-change-in-production")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"]       = False

    # ── Init extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # ── Register blueprints
    from server.routes.auth      import auth_bp
    from server.routes.chat      import chat_bp
    from server.routes.knowledge import kb_bp
    from server.routes.reminders import reminders_bp
    from server.routes.analytics import analytics_bp
    from server.routes.push      import push_bp
    from server.routes.admin      import admin_bp
    from server.routes.strategies import strategies_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(kb_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(push_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(strategies_bp)

    # ── Serve frontend at root
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    # ── Create tables and seed
    with app.app_context():
        db.create_all()
        # Import new models to ensure tables are created
        from server.models.announcement import Announcement, QueryLog  # noqa: F401
        db.create_all()
        from server.seed import seed_database
        seed_database()

    # ── APScheduler: start only once (not in Flask reloader parent process)
    main_proc = os.environ.get("WERKZEUG_RUN_MAIN")
    if main_proc == "true" or main_proc is None:
        from server.services.push_service import init_scheduler
        init_scheduler(app)

    return app
