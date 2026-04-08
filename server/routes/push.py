# ═══════════════════════════════════════════════════════════
# server/routes/push.py — Web Push Subscription Routes
# ═══════════════════════════════════════════════════════════

import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.extensions import db
from server.models.models import PushSubscription, User

push_bp = Blueprint("push", __name__, url_prefix="/api/push")


@push_bp.route("/vapid-public-key", methods=["GET"])
def vapid_public_key():
    key = os.environ.get("VAPID_PUBLIC_KEY", "")
    if not key:
        # Not an error — just tell the frontend push is unavailable
        return jsonify({"public_key": None, "available": False,
                        "message": "Push notifications not configured on this server."}), 200
    return jsonify({"public_key": key, "available": True}), 200


@push_bp.route("/subscribe", methods=["POST"])
@jwt_required()
def subscribe():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)
    if user.role != "student":
        return jsonify({"error": "Only students can subscribe."}), 403

    data   = request.get_json(silent=True)
    endpoint = (data.get("endpoint") or "").strip() if data else ""
    keys     = (data.get("keys")     or {})         if data else {}
    p256dh   = (keys.get("p256dh")   or "").strip()
    auth     = (keys.get("auth")     or "").strip()

    if not endpoint or not p256dh or not auth:
        return jsonify({"error": "Invalid subscription data."}), 400

    existing = PushSubscription.query.filter_by(endpoint=endpoint).first()
    if existing:
        existing.p256dh = p256dh; existing.auth = auth; existing.user_id = user_id
        db.session.commit()
        return jsonify({"message": "Subscription updated."}), 200

    db.session.add(PushSubscription(user_id=user_id, endpoint=endpoint, p256dh=p256dh, auth=auth))
    db.session.commit()
    return jsonify({"message": "Subscribed to push notifications."}), 201


@push_bp.route("/unsubscribe", methods=["POST"])
@jwt_required()
def unsubscribe():
    user_id  = int(get_jwt_identity())
    data     = request.get_json(silent=True)
    endpoint = ((data or {}).get("endpoint") or "").strip()
    sub = PushSubscription.query.filter_by(endpoint=endpoint, user_id=user_id).first()
    if sub:
        db.session.delete(sub); db.session.commit()
    return jsonify({"message": "Unsubscribed."}), 200


@push_bp.route("/status", methods=["GET"])
@jwt_required()
def status():
    user_id = int(get_jwt_identity())
    count   = PushSubscription.query.filter_by(user_id=user_id).count()
    key     = os.environ.get("VAPID_PUBLIC_KEY", "")
    return jsonify({"subscribed": count > 0, "count": count, "available": bool(key)}), 200


@push_bp.route("/test", methods=["POST"])
@jwt_required()
def test_push():
    user_id = int(get_jwt_identity())
    subs    = PushSubscription.query.filter_by(user_id=user_id).all()
    if not subs:
        return jsonify({"error": "No subscription found. Enable notifications first."}), 404
    from server.services.push_service import send_push
    sent = sum(1 for s in subs if send_push(s.to_webpush_sub(),
               "🔔 UPSA ITM Test", "Push notifications working!", "/#reminders"))
    return jsonify({"message": f"Test sent to {sent}/{len(subs)} subscription(s)."}), 200
