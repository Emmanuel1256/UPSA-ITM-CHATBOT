# ═══════════════════════════════════════════════════════════
# server/app.py — Flask Application Factory
# ═══════════════════════════════════════════════════════════

import os
from flask import Flask
from server.extensions import db, jwt, bcrypt, cors


def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "..", "client"),
        static_url_path=""
    )

    # ── Load .env if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # ── Configuration
    app.config["SECRET_KEY"]                   = os.environ.get("SECRET_KEY", "upsa-itm-secret-change-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"]      = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'upsa_itm.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"]               = os.environ.get("JWT_SECRET_KEY", "upsa-jwt-secret-change-in-production")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"]     = False   # tokens never expire (FYP demo)

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(kb_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(push_bp)

    # ── Serve frontend index.html at root
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    # ── Create all tables and seed on first run
    with app.app_context():
        db.create_all()
        from server.seed import seed_database
        seed_database()

    # ── Start APScheduler for daily push notifications
    # WERKZEUG_RUN_MAIN == "true"  → we are in the reloader child process  (start scheduler)
    # WERKZEUG_RUN_MAIN is absent  → we are running without the reloader   (start scheduler)
    # WERKZEUG_RUN_MAIN == other   → we are in the parent monitor process  (skip scheduler)
    main_proc = os.environ.get("WERKZEUG_RUN_MAIN")
    if main_proc == "true" or main_proc is None:
        from server.services.push_service import init_scheduler
        init_scheduler(app)

    return app