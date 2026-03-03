# ═══════════════════════════════════════════════════════════
# server/routes/chat.py
# Chat Routes — Send message, fetch history, clear history
# FR-3.x Core Chatbot | FR-2.x NLP Engine
# ═══════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.extensions import db
from server.models.models import ChatMessage, User, UnansweredQuery, IntentLog
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

    # ── NLP classification (queries live KnowledgeBase table)
    result = nlp_service.classify(text)

    if result["fallback"]:
        response_text = nlp_service.FALLBACK_RESPONSE
        # Log as unanswered query for lecturer analytics (FR-2.3)
        db.session.add(UnansweredQuery(
            question=text,
            student_level=user.level,
            user_id=user_id
        ))
    else:
        response_text = result["response"]
        # Log matched intent for analytics (FR-4.1)
        db.session.add(IntentLog(
            intent_name=result["intent"],
            user_id=user_id,
            user_level=user.level
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

    # ── Motivational message (~13% probability, FR-3.3)
    motivation = nlp_service.get_motivation()

    return jsonify({
        "user_message": user_msg.to_dict(),
        "bot_message":  bot_msg.to_dict(),
        "motivation":   motivation,
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