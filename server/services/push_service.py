# ═══════════════════════════════════════════════════════════
# server/services/push_service.py
# Smart Web Push Notification Service
#
# Scheduler fires every HOUR.
# For each reminder that falls within the next 3 days:
#   - If today is the activity day: notify at the exact activity time
#   - If within 3 days before:     notify at the same time each day
# This means students get notified at e.g. 14:00 on:
#   Day -3, Day -2, Day -1, and Day 0 (at the exact activity time)
# ═══════════════════════════════════════════════════════════

import os
import json
import logging
from datetime import date, datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval     import IntervalTrigger

logger = logging.getLogger(__name__)

VAPID_PRIVATE_KEY  = os.environ.get("VAPID_PRIVATE_KEY",  "")
VAPID_PUBLIC_KEY   = os.environ.get("VAPID_PUBLIC_KEY",   "")
VAPID_CLAIMS_EMAIL = os.environ.get("VAPID_CLAIMS_EMAIL", "mailto:admin@upsamail.edu.gh")

# Notify students on these days before (inclusive of day 0)
NOTIFY_DAYS_BEFORE = [3, 2, 1, 0]


def send_push(subscription_info: dict, title: str, body: str, url: str = "/") -> bool:
    """Send one Web Push notification. Returns True on success."""
    if not VAPID_PRIVATE_KEY or not VAPID_PUBLIC_KEY:
        logger.warning("[Push] VAPID keys not configured.")
        return False

    try:
        from pywebpush import webpush, WebPushException
        payload = json.dumps({
            "title": title,
            "body":  body,
            "url":   url,
            "icon":  "/icons/icon-192.png",
            "badge": "/icons/badge-72.png",
        })
        webpush(
            subscription_info=subscription_info,
            data=payload,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_CLAIMS_EMAIL},
        )
        return True
    except Exception as exc:
        status = str(exc)
        if "410" in status or "404" in status:
            logger.info(f"[Push] Expired subscription: {exc}")
        else:
            logger.error(f"[Push] Error: {exc}")
        return False


def check_and_notify(app):
    """
    Hourly scheduler job.
    Fires push notifications for upcoming reminders based on their exact time.

    Logic:
    - Get current Ghana time (Africa/Accra = UTC+0 normally, UTC+0 always — no DST)
    - For each reminder: if today is within NOTIFY_DAYS_BEFORE of the due date,
      AND the current hour matches the reminder's activity time hour → send push.
    """
    with app.app_context():
        from server.models.models import Reminder, PushSubscription, User
        from server.extensions import db

        now   = datetime.utcnow()   # Ghana is UTC+0 (no DST offset needed)
        today = now.date()
        current_hour = now.hour

        sent_count = 0
        stale_ids  = []

        for days_before in NOTIFY_DAYS_BEFORE:
            target_date = today + timedelta(days=days_before)
            reminders   = Reminder.query.filter_by(date=target_date).all()

            for reminder in reminders:
                # Parse the reminder's activity time (default 08:00)
                time_str     = reminder.time or "08:00"
                try:
                    activity_hour = int(time_str.split(":")[0])
                except (ValueError, IndexError):
                    activity_hour = 8

                # Only fire in the matching hour window
                if current_hour != activity_hour:
                    continue

                # Build notification text
                if days_before == 0:
                    urgency = f"TODAY at {time_str} 🔴"
                elif days_before == 1:
                    urgency = f"TOMORROW at {time_str} 🟡"
                else:
                    urgency = f"in {days_before} days ({target_date.strftime('%d %b')}) 🟢"

                title = f"⏰ {reminder.type.capitalize()} Reminder"
                body  = f"{reminder.title} — {urgency}. {reminder.description or ''}".strip()

                # Target students at matching level
                query = (
                    db.session.query(PushSubscription)
                    .join(User, User.id == PushSubscription.user_id)
                    .filter(User.role == "student")
                )
                if reminder.level != "all":
                    query = query.filter(User.level == reminder.level)

                for sub in query.all():
                    ok = send_push(
                        subscription_info=sub.to_webpush_sub(),
                        title=title,
                        body=body,
                        url="/#reminders",
                    )
                    if ok:
                        sent_count += 1
                    else:
                        stale_ids.append(sub.id)

        if stale_ids:
            PushSubscription.query.filter(
                PushSubscription.id.in_(stale_ids)
            ).delete(synchronize_session=False)
            db.session.commit()

        if sent_count:
            logger.info(f"[Push] Sent {sent_count} notification(s) at hour {current_hour}.")


def init_scheduler(app):
    """Start APScheduler — checks every hour for due notifications."""
    scheduler = BackgroundScheduler(timezone="UTC")

    scheduler.add_job(
        func=check_and_notify,
        args=[app],
        trigger=IntervalTrigger(hours=1),
        id="hourly_push_check",
        name="Hourly Reminder Push Notifications",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("[APScheduler] Started — hourly push notification checker running.")
    return scheduler
