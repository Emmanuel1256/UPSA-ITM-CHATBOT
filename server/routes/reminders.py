# ═══════════════════════════════════════════════════════════
# server/routes/reminders.py
# Reminders CRUD Routes
# CREATE/UPDATE/DELETE: lecturer only
# READ: any authenticated user (students filtered by level/semester)
# FR-3.2 Reminders Tab
# ═══════════════════════════════════════════════════════════

from datetime import date as Date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.extensions import db
from server.models.models import Reminder, User

reminders_bp = Blueprint("reminders", __name__, url_prefix="/api/reminders")

VALID_TYPES     = ("exam", "assignment", "project")
VALID_LEVELS    = ("all", "100", "200", "300")
VALID_SEMESTERS = ("1", "2")


# ─── GET ALL ─────────────────────────────────────────────────
@reminders_bp.route("/", methods=["GET"])
@jwt_required()
def get_reminders():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role == "student":
        # Students see only reminders for their level/semester or "all"
        items = (
            Reminder.query
            .filter(
                db.or_(Reminder.level == user.level, Reminder.level == "all"),
                Reminder.semester == user.semester,
            )
            .order_by(Reminder.date.asc())
            .all()
        )
    else:
        # Lecturers see all reminders
        items = Reminder.query.order_by(Reminder.date.asc()).all()

    return jsonify({"reminders": [r.to_dict() for r in items]}), 200


# ─── CREATE ──────────────────────────────────────────────────
@reminders_bp.route("/", methods=["POST"])
@jwt_required()
def create_reminder():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "lecturer":
        return jsonify({"error": "Only lecturers can create reminders."}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided."}), 400

    title       = (data.get("title")       or "").strip()
    description = (data.get("description") or "").strip()
    date_str    = (data.get("date")        or "").strip()
    level       = (data.get("level")       or "all").strip()
    semester    = str(data.get("semester") or "1").strip()
    rtype       = (data.get("type")        or "assignment").strip()

    if not title:
        return jsonify({"error": "Title is required."}), 400
    if not date_str:
        return jsonify({"error": "Date is required."}), 400
    if level not in VALID_LEVELS:
        return jsonify({"error": f"Level must be one of: {', '.join(VALID_LEVELS)}"}), 400
    if semester not in VALID_SEMESTERS:
        return jsonify({"error": "Semester must be 1 or 2."}), 400
    if rtype not in VALID_TYPES:
        return jsonify({"error": f"Type must be one of: {', '.join(VALID_TYPES)}"}), 400

    try:
        due_date = Date.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Date must be in YYYY-MM-DD format."}), 400

    reminder = Reminder(
        title=title,
        description=description,
        date=due_date,
        level=level,
        semester=semester,
        type=rtype,
        created_by=user_id,
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder created.", "reminder": reminder.to_dict()}), 201


# ─── UPDATE ──────────────────────────────────────────────────
@reminders_bp.route("/<int:rid>", methods=["PUT"])
@jwt_required()
def update_reminder(rid):
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "lecturer":
        return jsonify({"error": "Only lecturers can update reminders."}), 403

    reminder = Reminder.query.get_or_404(rid)
    data     = request.get_json(silent=True) or {}

    if "title" in data:
        t = data["title"].strip()
        if not t:
            return jsonify({"error": "Title cannot be empty."}), 400
        reminder.title = t

    if "description" in data:
        reminder.description = data["description"].strip()

    if "date" in data:
        try:
            reminder.date = Date.fromisoformat(data["date"])
        except ValueError:
            return jsonify({"error": "Date must be YYYY-MM-DD."}), 400

    if "level" in data:
        if data["level"] not in VALID_LEVELS:
            return jsonify({"error": "Invalid level."}), 400
        reminder.level = data["level"]

    if "semester" in data:
        if str(data["semester"]) not in VALID_SEMESTERS:
            return jsonify({"error": "Invalid semester."}), 400
        reminder.semester = str(data["semester"])

    if "type" in data:
        if data["type"] not in VALID_TYPES:
            return jsonify({"error": "Invalid type."}), 400
        reminder.type = data["type"]

    db.session.commit()
    return jsonify({"message": "Reminder updated.", "reminder": reminder.to_dict()}), 200


# ─── DELETE ──────────────────────────────────────────────────
@reminders_bp.route("/<int:rid>", methods=["DELETE"])
@jwt_required()
def delete_reminder(rid):
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "lecturer":
        return jsonify({"error": "Only lecturers can delete reminders."}), 403

    reminder = Reminder.query.get_or_404(rid)
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted."}), 200