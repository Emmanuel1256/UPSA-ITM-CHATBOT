# ═══════════════════════════════════════════════════════════
# server/routes/admin.py
# Lecturer Admin Routes
#   GET/POST/PUT/DELETE  /api/admin/knowledge  — KB management
#   GET                  /api/admin/insights   — top queries
#   GET/POST/DELETE      /api/admin/announcements
# ═══════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from server.extensions import db
from server.models.models import KnowledgeBase, User
from server.models.announcement import Announcement, QueryLog

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _require_lecturer():
    """Return (user, None) or (None, error_response)."""
    uid  = int(get_jwt_identity())
    user = User.query.get(uid)
    if not user or user.role not in ("lecturer", "admin"):
        return None, (jsonify({"error": "Lecturer access required."}), 403)
    return user, None


# ══════════════════════════════════════════════════════════════
#  KNOWLEDGE BASE MANAGEMENT
# ══════════════════════════════════════════════════════════════

@admin_bp.route("/knowledge", methods=["GET"])
@jwt_required()
def list_knowledge():
    user, err = _require_lecturer()
    if err: return err

    entries = KnowledgeBase.query.order_by(KnowledgeBase.intent_name).all()
    return jsonify({"entries": [e.to_dict() for e in entries]})


@admin_bp.route("/knowledge", methods=["POST"])
@jwt_required()
def add_knowledge():
    user, err = _require_lecturer()
    if err: return err

    data = request.get_json(silent=True) or {}
    intent_name   = (data.get("intent_name", "") or "").strip()
    keywords      = (data.get("keywords", "") or "").strip()
    response_text = (data.get("response_text", "") or "").strip()
    level         = (data.get("level", "all") or "all").strip()

    if not intent_name or not keywords or not response_text:
        return jsonify({"error": "intent_name, keywords, and response_text are required."}), 400

    if KnowledgeBase.query.filter_by(intent_name=intent_name).first():
        return jsonify({"error": f"Intent '{intent_name}' already exists."}), 409

    entry = KnowledgeBase(
        intent_name=intent_name,
        keywords=keywords,
        response_text=response_text,
        level=level,
        created_by=user.id,
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Entry added.", "entry": entry.to_dict()}), 201


@admin_bp.route("/knowledge/<int:entry_id>", methods=["PUT"])
@jwt_required()
def update_knowledge(entry_id):
    user, err = _require_lecturer()
    if err: return err

    entry = KnowledgeBase.query.get_or_404(entry_id)
    data  = request.get_json(silent=True) or {}

    if "keywords" in data:
        entry.keywords = data["keywords"].strip()
    if "response_text" in data:
        entry.response_text = data["response_text"].strip()
    if "level" in data:
        entry.level = data["level"].strip()
    if "intent_name" in data:
        entry.intent_name = data["intent_name"].strip()

    entry.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Entry updated.", "entry": entry.to_dict()})


@admin_bp.route("/knowledge/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def delete_knowledge(entry_id):
    user, err = _require_lecturer()
    if err: return err

    entry = KnowledgeBase.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Entry deleted."})


# ══════════════════════════════════════════════════════════════
#  QUERY INSIGHTS
# ══════════════════════════════════════════════════════════════

@admin_bp.route("/insights", methods=["GET"])
@jwt_required()
def query_insights():
    user, err = _require_lecturer()
    if err: return err

    # Top 20 most asked questions (by text similarity is complex — use raw count)
    from sqlalchemy import func, desc

    # Top intents
    top_intents = (
        db.session.query(QueryLog.intent, func.count(QueryLog.id).label("count"))
        .filter(QueryLog.intent.isnot(None))
        .group_by(QueryLog.intent)
        .order_by(desc("count"))
        .limit(20)
        .all()
    )

    # Fallback (unanswered) queries
    fallbacks = (
        QueryLog.query
        .filter_by(fallback=True)
        .order_by(QueryLog.timestamp.desc())
        .limit(20)
        .all()
    )

    # Total queries today vs all time
    from datetime import date
    today_start = datetime.combine(date.today(), datetime.min.time())
    total_all   = QueryLog.query.count()
    total_today = QueryLog.query.filter(QueryLog.timestamp >= today_start).count()

    return jsonify({
        "top_intents":   [{"intent": r.intent, "count": r.count} for r in top_intents],
        "fallbacks":     [q.to_dict() for q in fallbacks],
        "total_queries": total_all,
        "today_queries": total_today,
    })


# ══════════════════════════════════════════════════════════════
#  ANNOUNCEMENTS
# ══════════════════════════════════════════════════════════════

@admin_bp.route("/announcements", methods=["GET"])
@jwt_required()
def list_announcements():
    """Lecturers see all; students see only active ones."""
    uid  = int(get_jwt_identity())
    user = User.query.get_or_404(uid)

    if user.role in ("lecturer", "admin"):
        items = Announcement.query.order_by(Announcement.created_at.desc()).all()
    else:
        items = (Announcement.query
                 .filter_by(active=True)
                 .order_by(Announcement.created_at.desc())
                 .limit(5)
                 .all())

    return jsonify({"announcements": [a.to_dict() for a in items]})


@admin_bp.route("/announcements", methods=["POST"])
@jwt_required()
def post_announcement():
    user, err = _require_lecturer()
    if err: return err

    data = request.get_json(silent=True) or {}
    title = (data.get("title", "") or "").strip()
    body  = (data.get("body",  "") or "").strip()

    if not title or not body:
        return jsonify({"error": "title and body are required."}), 400

    ann = Announcement(title=title, body=body, author_id=user.id)
    db.session.add(ann)
    db.session.commit()

    # ── Push announcement to all subscribed students ───────
    try:
        import threading
        from flask import current_app
        from server.models.models import PushSubscription, User
        from server.services.push_service import send_push

        # Truncate body for notification (max 100 chars)
        preview = body if len(body) <= 100 else body[:97] + "…"
        push_title = f"📢 {title}"
        push_body  = preview
        push_url   = "/#chat"

        _app = current_app._get_current_object()

        def _push_to_students():
            with _app.app_context():
                student_subs = (
                    PushSubscription.query
                    .join(User, User.id == PushSubscription.user_id)
                    .filter(User.role == "student")
                    .all()
                )
                stale = []
                sent  = 0
                for sub in student_subs:
                    ok = send_push(sub.to_webpush_sub(), push_title, push_body, push_url)
                    if ok:   sent  += 1
                    else:    stale.append(sub.id)

                if stale:
                    PushSubscription.query.filter(
                        PushSubscription.id.in_(stale)
                    ).delete(synchronize_session=False)
                    db.session.commit()

                import logging
                logging.getLogger(__name__).info(
                    f"[Push] Announcement '{title}' sent to {sent} student(s)."
                )

        threading.Thread(target=_push_to_students, daemon=True).start()

    except Exception as _pe:
        pass  # Never block the announcement save due to push failure

    return jsonify({"message": "Announcement posted.", "announcement": ann.to_dict()}), 201


@admin_bp.route("/announcements/<int:ann_id>", methods=["PUT"])
@jwt_required()
def edit_announcement(ann_id):
    user, err = _require_lecturer()
    if err: return err
    ann  = Announcement.query.get_or_404(ann_id)
    data = request.get_json(silent=True) or {}
    title = (data.get("title", "") or "").strip()
    body  = (data.get("body",  "") or "").strip()
    if not title or not body:
        return jsonify({"error": "title and body are required."}), 400
    ann.title = title
    ann.body  = body
    db.session.commit()
    return jsonify({"message": "Announcement updated.", "announcement": ann.to_dict()})


@admin_bp.route("/announcements/<int:ann_id>", methods=["DELETE"])
@jwt_required()
def delete_announcement(ann_id):
    user, err = _require_lecturer()
    if err: return err

    ann = Announcement.query.get_or_404(ann_id)
    db.session.delete(ann)
    db.session.commit()
    return jsonify({"message": "Announcement deleted."})


@admin_bp.route("/announcements/<int:ann_id>/toggle", methods=["POST"])
@jwt_required()
def toggle_announcement(ann_id):
    user, err = _require_lecturer()
    if err: return err

    ann = Announcement.query.get_or_404(ann_id)
    ann.active = not ann.active
    db.session.commit()
    return jsonify({"message": "Toggled.", "active": ann.active})
