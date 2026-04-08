# ═══════════════════════════════════════════════════════════
# server/extensions.py
# Flask extensions — instantiated here, registered in app.py
# Keeping them here prevents circular import issues between
# app.py → routes → models → extensions
# ═══════════════════════════════════════════════════════════

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db     = SQLAlchemy()
jwt    = JWTManager()
bcrypt = Bcrypt()
cors   = CORS()
