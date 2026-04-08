# ═══════════════════════════════════════════════════════════
# server/routes/chat.py
# Chat Routes — Send message, fetch history, clear history
# FR-3.x Core Chatbot | FR-2.x NLP Engine
# ═══════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.extensions import db
from server.models.models import ChatMessage, User, UnansweredQuery, IntentLog
from server.models.announcement import QueryLog
from server.services import nlp_service

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")

# Max message pairs retained per student (FR-1.3)
SESSION_HISTORY_LIMIT = 10


# ─── SEND MESSAGE ────────────────────────────────────────────
@chat_bp.route("/message", methods=["POST"])
@jwt_required()
def send_message():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "student":
        return jsonify({"error": "Only students can use the chat."}), 403

    data = request.get_json(silent=True)
    text = (data.get("message") or "").strip() if data else ""
    if not text:
        return jsonify({"error": "Message cannot be empty."}), 400

    # ── Save user message
    user_msg = ChatMessage(user_id=user_id, role="user", content=text)
    db.session.add(user_msg)

    # ── NLP classification — pass student level for level-aware filtering
    result = nlp_service.classify(text, student_level=user.level or "100")

    resource_url = None
    if result["fallback"]:
        response_text = nlp_service.FALLBACK_RESPONSE
        # Log as unanswered query for lecturer analytics (FR-2.3)
        db.session.add(UnansweredQuery(
            question=text,
            student_level=user.level,
            user_id=user_id
        ))
        # Push immediate alert to all subscribed lecturers (FR-3.4)
        try:
            from flask import current_app
            from server.services.push_service import notify_lecturers_unanswered
            # Run in a thread so the student response is not delayed
            import threading
            _app = current_app._get_current_object()
            threading.Thread(
                target=notify_lecturers_unanswered,
                args=(_app, text, user.level or "?"),
                daemon=True
            ).start()
        except Exception as _pe:
            pass  # Never block the chat response due to push failure
    else:
        response_text = result["response"]
        # Attach resource recommendation from knowledge base entry (FR-3.4)
        from server.models.models import KnowledgeBase
        kb_entry = KnowledgeBase.query.filter_by(intent_name=result["intent"]).first()
        if kb_entry and kb_entry.resource_url:
            resource_url = kb_entry.resource_url
        # Log matched intent for analytics (FR-4.1)
        db.session.add(IntentLog(
            intent_name=result["intent"],
            user_id=user_id,
            user_level=user.level
        ))

    # ── Always log to QueryLog for lecturer insights
    db.session.add(QueryLog(
        query_text=text,
        intent=result.get("intent"),
        confidence=result.get("confidence"),
        fallback=result["fallback"],
        user_level=user.level,
    ))

    # ── Save assistant response
    bot_msg = ChatMessage(
        user_id=user_id,
        role="assistant",
        content=response_text,
        intent=result.get("intent"),
        confidence=result.get("confidence"),
        fallback=result["fallback"],
    )
    db.session.add(bot_msg)

    # ── Enforce history limit — trim oldest pairs if over limit
    all_msgs = (
        ChatMessage.query
        .filter_by(user_id=user_id)
        .order_by(ChatMessage.id.asc())
        .all()
    )
    if len(all_msgs) > SESSION_HISTORY_LIMIT * 2:
        excess = len(all_msgs) - SESSION_HISTORY_LIMIT * 2
        for old in all_msgs[:excess]:
            db.session.delete(old)

    db.session.commit()

    resp = bot_msg.to_dict()
    if resource_url:
        resp["resource_url"] = resource_url

    return jsonify({
        "user_message": user_msg.to_dict(),
        "bot_message":  resp,
    }), 200


# ─── GET HISTORY ─────────────────────────────────────────────
@chat_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "student":
        return jsonify({"error": "Only students have chat history."}), 403

    messages = (
        ChatMessage.query
        .filter_by(user_id=user_id)
        .order_by(ChatMessage.timestamp.asc())
        .all()
    )
    return jsonify({"messages": [m.to_dict() for m in messages]}), 200


# ─── CLEAR HISTORY ───────────────────────────────────────────
@chat_bp.route("/history", methods=["DELETE"])
@jwt_required()
def clear_history():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "student":
        return jsonify({"error": "Forbidden."}), 403

    ChatMessage.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"message": "Chat history cleared."}), 200


# ─── GREETING (on login) ─────────────────────────────────────
# Returns a motivational phrase + upcoming reminders for the student
# Called once from the frontend when the student logs in
@chat_bp.route("/greeting", methods=["GET"])
@jwt_required()
def greeting():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "student":
        return jsonify({"error": "Students only."}), 403

    from server.models.models import Reminder
    from datetime import date, timedelta, datetime

    # ── Track login time + detect inactivity for tailored motivation ──
    now = datetime.utcnow()
    days_away = None
    if user.last_login:
        days_away = (now - user.last_login).days
    user.last_login = now
    db.session.add(user)
    db.session.commit()

    # Fetch upcoming reminders in the next 14 days matching the student's level
    today     = date.today()
    lookahead = today + timedelta(days=14)

    upcoming = (
        Reminder.query
        .filter(
            Reminder.date >= today,
            Reminder.date <= lookahead,
            db.or_(Reminder.level == user.level, Reminder.level == "all"),
            Reminder.semester == user.semester,
        )
        .order_by(Reminder.date.asc())
        .limit(5)
        .all()
    )

    upcoming_list = []
    for r in upcoming:
        delta = (r.date - today).days
        if delta == 0:
            when = "Today"
        elif delta == 1:
            when = "Tomorrow"
        else:
            when = f"In {delta} days"
        upcoming_list.append({
            "title": r.title,
            "date":  r.date.isoformat(),
            "time":  r.time or "08:00",
            "type":  r.type,
            "when":  when,
        })

    # ── Motivation: event-triggered (inactivity) or standard ──────────
    from server.models.models import Motivation
    import random

    INACTIVITY_PROMPTS = [
        "Welcome back! Even a short coding session keeps the momentum going. What shall we tackle today?",
        "It's been a few days — that's okay! Every expert was once a beginner who kept showing up.",
        "Great to see you back! Consistent effort, even in small steps, is what separates good developers from great ones.",
        "You returned — that's the hardest part. Let's pick up where you left off!",
    ]

    if days_away is not None and days_away >= 3:
        # Inactivity-triggered motivational prompt (FR-2.1)
        motivation = random.choice(INACTIVITY_PROMPTS)
        inactivity_flag = True
    else:
        motivation = nlp_service.get_motivation()
        if not motivation:
            all_motivations = Motivation.query.all()
            if all_motivations:
                motivation = random.choice(all_motivations).message
        inactivity_flag = False

    # ── Deadline proximity — urgent nudge if something is due ≤ 3 days ─
    urgent = next((r for r in upcoming_list if r["when"] in ("Today", "Tomorrow", "In 2 days", "In 3 days")), None)
    deadline_nudge = None
    if urgent:
        deadline_nudge = f"⚠️ Heads up! '{urgent['title']}' is due {urgent['when'].lower()}. Make sure you're on track!"

    # Fetch active announcements from lecturers
    from server.models.announcement import Announcement
    announcements = (
        Announcement.query
        .filter_by(active=True)
        .order_by(Announcement.created_at.desc())
        .limit(3)
        .all()
    )

    return jsonify({
        "motivation":      motivation,
        "inactivity":      inactivity_flag,
        "deadline_nudge":  deadline_nudge,
        "upcoming":        upcoming_list,
        "name":            user.name.split()[0],
        "announcements":   [a.to_dict() for a in announcements],
    }), 200
