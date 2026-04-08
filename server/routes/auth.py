# ═══════════════════════════════════════════════════════════
# server/routes/auth.py
# Authentication Routes — Register, Login, Me
# FR-1.1 Student Profile | FR-1.2 Lecturer Auth
# ═══════════════════════════════════════════════════════════

import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from server.extensions import db, bcrypt
from server.models.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# ─── UPSA Email Validation Rules ────────────────────────────
#
# Student  → exactly 8 digits before @upsamail.edu.gh
#   Regex  : ^\d{8}@upsamail\.edu\.gh$
#   ✅ 10299860@upsamail.edu.gh
#   ❌ 1029986@upsamail.edu.gh   (7 digits)
#   ❌ john.doe@upsamail.edu.gh  (not digits)
#
# Lecturer → firstname.lastname — letters only, one dot, ≥2 chars each part
#   Regex  : ^[a-z]{2,}\.[a-z]{2,}@upsamail\.edu\.gh$
#   ✅ john.doe@upsamail.edu.gh
#   ✅ kwame.mensah@upsamail.edu.gh
#   ❌ john123.doe@upsamail.edu.gh  (digit in name)
#   ❌ j.doe@upsamail.edu.gh        (firstname < 2 chars)
#   ❌ 10299860@upsamail.edu.gh     (student ID rejected)
# ────────────────────────────────────────────────────────────

STUDENT_EMAIL_RE  = re.compile(r"^\d{8}@upsamail\.edu\.gh$")
LECTURER_EMAIL_RE = re.compile(r"^[a-z]{2,}\.[a-z]{2,}@upsamail\.edu\.gh$")


def validate_upsa_email(email: str, role: str) -> tuple:
    """
    Validate email against UPSA institutional format for the given role.
    Returns (True, "") on success, (False, error_message) on failure.
    """
    email = email.strip().lower()

    if not email.endswith("@upsamail.edu.gh"):
        return False, (
            "Only UPSA institutional emails are accepted. "
            "Use your @upsamail.edu.gh address."
        )

    local = email.split("@")[0]

    if role == "student":
        if not STUDENT_EMAIL_RE.match(email):
            if not local.isdigit():
                return False, (
                    "Student email must be your 8-digit student ID followed by "
                    "@upsamail.edu.gh — e.g. 10299860@upsamail.edu.gh"
                )
            if len(local) < 8:
                return False, (
                    f"Your student ID appears too short ({len(local)} digits). "
                    "A valid student ID has exactly 8 digits."
                )
            if len(local) > 8:
                return False, (
                    f"Your student ID appears too long ({len(local)} digits). "
                    "A valid student ID has exactly 8 digits."
                )
            return False, "Invalid student email format. Use: 10299860@upsamail.edu.gh"

    elif role == "lecturer":
        if local.isdigit():
            return False, (
                "That looks like a student ID. Lecturer email must be "
                "firstname.lastname@upsamail.edu.gh — e.g. john.doe@upsamail.edu.gh"
            )
        if "." not in local:
            return False, (
                "Lecturer email must include a dot between first and last name. "
                "Format: firstname.lastname@upsamail.edu.gh"
            )
        if local.count(".") > 1:
            return False, (
                "Lecturer email must contain exactly one dot separating firstname and lastname."
            )
        if not LECTURER_EMAIL_RE.match(email):
            parts = local.split(".")
            if any(c.isdigit() for c in local):
                return False, "Lecturer email must contain only letters — no numbers allowed."
            if len(parts[0]) < 2:
                return False, "Your first name in the email must be at least 2 letters."
            if len(parts[1]) < 2:
                return False, "Your last name in the email must be at least 2 letters."
            return False, (
                "Lecturer email must be firstname.lastname@upsamail.edu.gh — "
                "letters only, no numbers or special characters."
            )
    else:
        return False, "Invalid role specified."

    return True, ""


# ─── REGISTER ───────────────────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided."}), 400

    name     = (data.get("name")     or "").strip()
    email    = (data.get("email")    or "").strip().lower()
    password = (data.get("password") or "")
    role     = (data.get("role")     or "").strip().lower()
    level    = (data.get("level")    or None)
    semester = (data.get("semester") or None)

    if not name:
        return jsonify({"error": "Full name is required."}), 400
    if len(name) < 3:
        return jsonify({"error": "Name must be at least 3 characters."}), 400
    if role not in ("student", "lecturer"):
        return jsonify({"error": "Role must be 'student' or 'lecturer'."}), 400
    if role == "student" and level not in ("100", "200", "300"):
        return jsonify({"error": "Please select a valid level (100, 200, or 300)."}), 400
    if role == "student" and str(semester) not in ("1", "2"):
        return jsonify({"error": "Please select a valid semester (1 or 2)."}), 400

    valid, err = validate_upsa_email(email, role)
    if not valid:
        return jsonify({"error": err}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role,
        level=level        if role == "student" else None,
        semester=str(semester) if role == "student" else None,
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Account created successfully.",
        "token":   token,
        "user":    user.to_dict(),
    }), 201


# ─── LOGIN ──────────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided."}), 400

    email    = (data.get("email")    or "").strip().lower()
    password = (data.get("password") or "")
    role     = (data.get("role")     or "").strip().lower()

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    if role not in ("student", "lecturer"):
        return jsonify({"error": "Invalid role."}), 400

    valid, err = validate_upsa_email(email, role)
    if not valid:
        return jsonify({"error": err}), 400

    user = User.query.filter_by(email=email, role=role).first()
    if not user:
        return jsonify({"error": "No account found with this email and role."}), 401

    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Incorrect password."}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful.",
        "token":   token,
        "user":    user.to_dict(),
    }), 200


# ─── ME ─────────────────────────────────────────────────────
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)
    return jsonify({"user": user.to_dict()}), 200
