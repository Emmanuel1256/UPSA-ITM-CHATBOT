# ═══════════════════════════════════════════════════════════
# server/routes/push.py
# Web Push Subscription Routes
# Students subscribe/unsubscribe from browser push notifications
# ═══════════════════════════════════════════════════════════

import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.extensions import db
from server.models.models import PushSubscription, User

push_bp = Blueprint("push", __name__, url_prefix="/api/push")


# ─── VAPID PUBLIC KEY ─────────────────────────────────────────
# No JWT required — frontend needs this BEFORE login to set up SW
@push_bp.route("/vapid-public-key", methods=["GET"])
def vapid_public_key():
    key = os.environ.get("VAPID_PUBLIC_KEY", "")
    if not key:
        return jsonify({"error": "Push notifications not configured on this server."}), 503
    return jsonify({"public_key": key}), 200


# ─── SUBSCRIBE ────────────────────────────────────────────────
@push_bp.route("/subscribe", methods=["POST"])
@jwt_required()
def subscribe():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != "student":
        return jsonify({"error": "Only students can subscribe to push notifications."}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No subscription data provided."}), 400

    endpoint = (data.get("endpoint") or "").strip()
    keys     = data.get("keys") or {}
    p256dh   = (keys.get("p256dh") or "").strip()
    auth     = (keys.get("auth")   or "").strip()

    if not endpoint or not p256dh or not auth:
        return jsonify({"error": "Invalid subscription — endpoint, p256dh, and auth are required."}), 400

    # Upsert — update if already exists, otherwise create
    existing = PushSubscription.query.filter_by(endpoint=endpoint).first()
    if existing:
        existing.p256dh  = p256dh
        existing.auth    = auth
        existing.user_id = user_id
        db.session.commit()
        return jsonify({"message": "Push subscription updated."}), 200

    sub = PushSubscription(
        user_id=user_id,
        endpoint=endpoint,
        p256dh=p256dh,
        auth=auth,
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "Push subscription saved. You will receive reminder notifications."}), 201


# ─── UNSUBSCRIBE ──────────────────────────────────────────────
@push_bp.route("/unsubscribe", methods=["POST"])
@jwt_required()
def unsubscribe():
    user_id  = int(get_jwt_identity())
    data     = request.get_json(silent=True)
    endpoint = ((data or {}).get("endpoint") or "").strip()

    if not endpoint:
        return jsonify({"error": "Endpoint is required."}), 400

    sub = PushSubscription.query.filter_by(endpoint=endpoint, user_id=user_id).first()
    if sub:
        db.session.delete(sub)
        db.session.commit()

    return jsonify({"message": "Unsubscribed from push notifications."}), 200


# ─── SUBSCRIPTION STATUS ──────────────────────────────────────
@push_bp.route("/status", methods=["GET"])
@jwt_required()
def status():
    user_id = int(get_jwt_identity())
    count   = PushSubscription.query.filter_by(user_id=user_id).count()
    return jsonify({"subscribed": count > 0, "count": count}), 200


# ─── TEST PUSH ────────────────────────────────────────────────
@push_bp.route("/test", methods=["POST"])
@jwt_required()
def test_push():
    """Send a test notification to the current user. Useful to verify setup."""
    user_id = int(get_jwt_identity())
    subs    = PushSubscription.query.filter_by(user_id=user_id).all()

    if not subs:
        return jsonify({"error": "No push subscription found. Enable notifications first."}), 404

    from server.services.push_service import send_push
    sent = 0
    for sub in subs:
        ok = send_push(
            subscription_info=sub.to_webpush_sub(),
            title="🔔 UPSA ITM — Test Notification",
            body="Push notifications are working! You will receive reminders 3 and 1 day before due dates.",
            url="/#reminders",
        )
        if ok:
            sent += 1

    return jsonify({"message": f"Test notification sent to {sent}/{len(subs)} subscription(s)."}), 200