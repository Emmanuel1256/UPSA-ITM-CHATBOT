# ═══════════════════════════════════════════════════════════
# server/routes/reminders.py
# Reminders CRUD + Semester Planner Routes
# ═══════════════════════════════════════════════════════════

from datetime import date as Date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.extensions import db
from server.models.models import Reminder, User

reminders_bp = Blueprint("reminders", __name__, url_prefix="/api/reminders")

VALID_TYPES     = ("exam", "assignment", "project", "lecture", "quiz", "lab")
VALID_LEVELS    = ("all", "100", "200", "300")
VALID_SEMESTERS = ("1", "2")


@reminders_bp.route("/", methods=["GET"])
@jwt_required()
def get_reminders():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role == "student":
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
        items = Reminder.query.order_by(Reminder.week.asc(), Reminder.date.asc()).all()

    return jsonify({"reminders": [r.to_dict() for r in items]}), 200


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
    time_str    = (data.get("time")        or "08:00").strip()
    level       = (data.get("level")       or "all").strip()
    semester    = str(data.get("semester") or "1").strip()
    rtype       = (data.get("type")        or "assignment").strip()
    week        = data.get("week")

    if not title:   return jsonify({"error": "Title is required."}), 400
    if not date_str: return jsonify({"error": "Date is required."}), 400
    if level    not in VALID_LEVELS:    return jsonify({"error": "Invalid level."}), 400
    if semester not in VALID_SEMESTERS: return jsonify({"error": "Invalid semester."}), 400
    if rtype    not in VALID_TYPES:     return jsonify({"error": f"Type must be one of: {', '.join(VALID_TYPES)}"}), 400

    try:
        due_date = Date.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Date must be YYYY-MM-DD."}), 400

    reminder = Reminder(
        title=title, description=description, date=due_date,
        time=time_str, level=level, semester=semester, type=rtype,
        week=int(week) if week else None, created_by=user_id,
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder created.", "reminder": reminder.to_dict()}), 201


@reminders_bp.route("/<int:rid>", methods=["PUT"])
@jwt_required()
def update_reminder(rid):
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)
    if user.role != "lecturer":
        return jsonify({"error": "Only lecturers can update reminders."}), 403

    reminder = Reminder.query.get_or_404(rid)
    data     = request.get_json(silent=True) or {}

    if "title"       in data: reminder.title       = data["title"].strip()
    if "description" in data: reminder.description = data["description"].strip()
    if "time"        in data: reminder.time        = data["time"].strip()
    if "week"        in data: reminder.week        = int(data["week"]) if data["week"] else None
    if "date" in data:
        try:    reminder.date = Date.fromisoformat(data["date"])
        except: return jsonify({"error": "Date must be YYYY-MM-DD."}), 400
    if "level"    in data: reminder.level    = data["level"]
    if "semester" in data: reminder.semester = str(data["semester"])
    if "type"     in data: reminder.type     = data["type"]

    db.session.commit()
    return jsonify({"message": "Reminder updated.", "reminder": reminder.to_dict()}), 200


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


# ── Bulk create for semester planner ─────────────────────────
@reminders_bp.route("/bulk", methods=["POST"])
@jwt_required()
def bulk_create():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)
    if user.role != "lecturer":
        return jsonify({"error": "Lecturer access required."}), 403

    data  = request.get_json(silent=True) or {}
    items = data.get("reminders", [])
    if not items:
        return jsonify({"error": "No reminders provided."}), 400

    created = 0
    for item in items:
        try:
            due_date = Date.fromisoformat(item.get("date", ""))
        except (ValueError, TypeError):
            continue
        reminder = Reminder(
            title       = (item.get("title") or "").strip(),
            description = (item.get("description") or "").strip(),
            date        = due_date,
            time        = item.get("time", "08:00"),
            level       = item.get("level", "all"),
            semester    = str(item.get("semester", "1")),
            type        = item.get("type", "lecture"),
            week        = item.get("week"),
            created_by  = user_id,
        )
        if reminder.title:
            db.session.add(reminder)
            created += 1

    db.session.commit()
    return jsonify({"message": f"{created} reminders saved.", "created": created}), 201


# ─── GET PLANNER (all week-assigned reminders, lecturer only) ───
@reminders_bp.route("/planner", methods=["GET"])
@jwt_required()
def get_planner():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "lecturer":
        return jsonify({"error": "Lecturer access only."}), 403

    semester = request.args.get("semester", "1")

    items = (
        Reminder.query
        .filter(
            Reminder.week.isnot(None),
            Reminder.semester == semester,
        )
        .order_by(Reminder.week.asc(), Reminder.date.asc(), Reminder.time.asc())
        .all()
    )

    return jsonify({"reminders": [r.to_dict() for r in items]}), 200
