# ═══════════════════════════════════════════════════════════
# server/routes/strategies.py
# Weekly Strategy Routes
#   GET  /api/strategies?course=&level=       — full 13-week plan
#   GET  /api/strategies/week?course=&level=&week=  — single week
#   PUT  /api/strategies/<id>                 — lecturer edits strategy
#   POST /api/strategies                      — lecturer adds new entry
# ═══════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from server.extensions import db
from server.models.models import User
from server.models.strategy import WeeklyStrategy

strategies_bp = Blueprint("strategies", __name__, url_prefix="/api/strategies")


def _get_user():
    uid = int(get_jwt_identity())
    return User.query.get(uid)


# ── GET full 13-week plan for a course + level ──────────────
@strategies_bp.route("", methods=["GET"])
@jwt_required()
def get_strategies():
    course = request.args.get("course", "").strip().lower()
    level  = request.args.get("level",  "").strip()

    if not course or not level:
        return jsonify({"error": "course and level are required."}), 400

    entries = (
        WeeklyStrategy.query
        .filter_by(course=course, level=level)
        .order_by(WeeklyStrategy.week)
        .all()
    )
    return jsonify({"strategies": [e.to_dict() for e in entries]})


# ── GET single week strategy ────────────────────────────────
@strategies_bp.route("/week", methods=["GET"])
@jwt_required()
def get_week_strategy():
    course = request.args.get("course", "").strip().lower()
    level  = request.args.get("level",  "").strip()
    week   = request.args.get("week",   "").strip()

    entry = WeeklyStrategy.query.filter_by(
        course=course, level=level, week=int(week)
    ).first()

    if not entry:
        return jsonify({"strategy": None}), 200

    return jsonify({"strategy": entry.to_dict()})


# ── PUT — lecturer updates a strategy ──────────────────────
@strategies_bp.route("/<int:sid>", methods=["PUT"])
@jwt_required()
def update_strategy(sid):
    user = _get_user()
    if not user or user.role not in ("lecturer", "admin"):
        return jsonify({"error": "Lecturer access required."}), 403

    entry = WeeklyStrategy.query.get_or_404(sid)
    data  = request.get_json(silent=True) or {}

    if "topic"       in data: entry.topic       = data["topic"].strip()
    if "activity"    in data: entry.activity     = data["activity"].strip()
    if "strategy"    in data: entry.strategy     = data["strategy"].strip()
    if "evening_tip" in data: entry.evening_tip  = data["evening_tip"].strip()
    entry.updated_at  = datetime.utcnow()
    entry.created_by  = user.id

    db.session.commit()
    return jsonify({"message": "Strategy updated.", "strategy": entry.to_dict()})


# ── POST — lecturer adds a new strategy entry ───────────────
@strategies_bp.route("", methods=["POST"])
@jwt_required()
def add_strategy():
    user = _get_user()
    if not user or user.role not in ("lecturer", "admin"):
        return jsonify({"error": "Lecturer access required."}), 403

    data    = request.get_json(silent=True) or {}
    course  = (data.get("course",  "") or "").strip().lower()
    level   = (data.get("level",   "") or "").strip()
    week    = data.get("week")
    topic   = (data.get("topic",   "") or "").strip()
    activity= (data.get("activity","lecture") or "lecture").strip()
    strategy= (data.get("strategy","") or "").strip()
    evening = (data.get("evening_tip","") or "").strip()

    if not all([course, level, week, topic, strategy]):
        return jsonify({"error": "course, level, week, topic and strategy are required."}), 400

    # Check for duplicate
    exists = WeeklyStrategy.query.filter_by(
        course=course, level=level, week=int(week)
    ).first()
    if exists:
        return jsonify({"error": f"Week {week} entry for {course} L{level} already exists. Use PUT to update."}), 409

    entry = WeeklyStrategy(
        course=course, level=level, week=int(week),
        topic=topic, activity=activity,
        strategy=strategy, evening_tip=evening,
        created_by=user.id
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Strategy added.", "strategy": entry.to_dict()}), 201


# ── GET all courses + levels (for lecturer picker) ──────────
@strategies_bp.route("/courses", methods=["GET"])
@jwt_required()
def list_courses():
    return jsonify({
        "courses": [
            {"id": "programming", "label": "Programming"},
            {"id": "database",    "label": "Database Management"},
            {"id": "networking",  "label": "Networking"},
        ],
        "levels": ["100", "200", "300"]
    })
