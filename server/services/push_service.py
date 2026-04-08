# ═══════════════════════════════════════════════════════════
# server/services/push_service.py
# Smart Push Notification Service
# - Fires hourly
# - Notifies at the exact activity time on days 3, 2, 1, 0
# - Gracefully skips if VAPID keys not configured (no crash)
# ═══════════════════════════════════════════════════════════

import os
import json
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval     import IntervalTrigger

logger = logging.getLogger(__name__)

# Load and normalise VAPID keys
# python-dotenv stores multi-line PEM as literal \n — convert back to real newlines
_raw_private = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_PRIVATE_KEY  = _raw_private.replace("\\n", "\n") if _raw_private else ""
VAPID_PUBLIC_KEY   = os.environ.get("VAPID_PUBLIC_KEY",   "")
VAPID_CLAIMS_EMAIL = os.environ.get("VAPID_CLAIMS_EMAIL", "mailto:admin@upsamail.edu.gh")

NOTIFY_DAYS_BEFORE = [3, 2, 1, 0]


def push_configured() -> bool:
    return bool(VAPID_PRIVATE_KEY and VAPID_PUBLIC_KEY)


def send_push(subscription_info: dict, title: str, body: str, url: str = "/") -> bool:
    if not push_configured():
        return False
    try:
        from pywebpush import webpush, WebPushException
        payload = json.dumps({"title": title, "body": body, "url": url,
                               "icon": "/icons/icon-192.png", "badge": "/icons/badge-72.png"})
        webpush(subscription_info=subscription_info, data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={"sub": VAPID_CLAIMS_EMAIL})
        return True
    except Exception as exc:
        s = str(exc)
        if "410" in s or "404" in s:
            logger.info(f"[Push] Expired subscription removed: {exc}")
        else:
            logger.error(f"[Push] Error: {exc}")
        return False


def check_and_notify(app):
    with app.app_context():
        from server.models.models import Reminder, PushSubscription, User
        from server.extensions import db

        if not push_configured():
            return   # VAPID not set up — skip silently

        now          = datetime.utcnow()
        today        = now.date()
        current_hour = now.hour
        sent_count   = 0
        stale_ids    = []

        for days_before in NOTIFY_DAYS_BEFORE:
            target_date = today + timedelta(days=days_before)
            reminders   = Reminder.query.filter_by(date=target_date).all()

            for reminder in reminders:
                time_str = reminder.time or "08:00"
                try:
                    activity_hour = int(time_str.split(":")[0])
                except (ValueError, IndexError):
                    activity_hour = 8

                if current_hour != activity_hour:
                    continue

                if days_before == 0:
                    urgency = f"TODAY at {time_str} 🔴"
                elif days_before == 1:
                    urgency = f"TOMORROW at {time_str} 🟡"
                else:
                    urgency = f"in {days_before} days ({target_date.strftime('%d %b')}) 🟢"

                title = f"⏰ {reminder.type.capitalize()} Reminder — Week {reminder.week or '?'}"
                base_body = f"{reminder.title} — {urgency}. {reminder.description or ''}".strip()

                # Attach strategy excerpt if available for the week's course + level
                strategy_tip = ""
                try:
                    from server.models.strategy import WeeklyStrategy
                    # Map reminder course to strategy course key
                    course_map = {
                        "programming": "programming",
                        "database": "database",
                        "database management": "database",
                        "networking": "networking",
                    }
                    course_key = course_map.get(
                        (reminder.type or "").lower().split()[0], None
                    )
                    if course_key and reminder.week:
                        # Get level from subscriber's user record
                        strat = WeeklyStrategy.query.filter_by(
                            course=course_key,
                            week=reminder.week
                        ).first()
                        if strat:
                            tip = strat.strategy[:120].rstrip()
                            strategy_tip = f" 💡 {tip}…"
                except Exception:
                    pass

                body = base_body + strategy_tip

                query = (db.session.query(PushSubscription)
                           .join(User, User.id == PushSubscription.user_id)
                           .filter(User.role == "student"))
                if reminder.level != "all":
                    query = query.filter(User.level == reminder.level)

                for sub in query.all():
                    ok = send_push(sub.to_webpush_sub(), title, body, "/#reminders")
                    if ok:   sent_count += 1
                    else:    stale_ids.append(sub.id)

        if stale_ids:
            PushSubscription.query.filter(
                PushSubscription.id.in_(stale_ids)
            ).delete(synchronize_session=False)
            db.session.commit()

        if sent_count:
            logger.info(f"[Push] Sent {sent_count} notification(s) at hour {current_hour}.")


def send_daily_motivation(app):
    """
    Fires daily at 08:00 UTC.
    Sends a random motivational message to ALL subscribed students.
    """
    with app.app_context():
        from server.models.models import PushSubscription, Motivation, User
        if not push_configured():
            return

        motivations = Motivation.query.all()
        if not motivations:
            return

        import random
        message = random.choice(motivations).message
        title   = "💡 Good Morning from UPSA ITM!"
        body    = message

        subs = (PushSubscription.query
                .join(User, User.id == PushSubscription.user_id)
                .filter(User.role == "student")
                .all())

        sent = sum(1 for s in subs if send_push(s.to_webpush_sub(), title, body, "/"))
        logger.info(f"[Push] Daily motivation sent to {sent} student(s).")


def notify_lecturers_unanswered(app, query_text: str, student_level: str = "?"):
    """
    Immediately push all subscribed lecturers when a student asks a question
    the NLP engine cannot answer (fallback = True).
    Called directly from the chat route — NOT via the scheduler.
    """
    with app.app_context():
        from server.models.models import PushSubscription, User
        from server.extensions import db

        if not push_configured():
            return

        title = "❓ Unanswered Student Query"
        # Trim long queries for the notification body
        short = query_text if len(query_text) <= 80 else query_text[:77] + "…"
        body  = f"Level {student_level} student asked: \"{short}\". Consider adding this to the Knowledge Base."

        lecturer_subs = (
            PushSubscription.query
            .join(User, User.id == PushSubscription.user_id)
            .filter(User.role == "lecturer")
            .all()
        )

        stale = []
        sent  = 0
        for sub in lecturer_subs:
            ok = send_push(sub.to_webpush_sub(), title, body, "/#admin")
            if ok:   sent  += 1
            else:    stale.append(sub.id)

        if stale:
            PushSubscription.query.filter(
                PushSubscription.id.in_(stale)
            ).delete(synchronize_session=False)
            db.session.commit()

        if sent:
            logger.info(f"[Push] Unanswered-query alert sent to {sent} lecturer(s).")


def init_scheduler(app):
    from apscheduler.triggers.cron import CronTrigger

    scheduler = BackgroundScheduler(timezone="UTC")

    # Hourly — check for upcoming activity reminders
    scheduler.add_job(
        func=check_and_notify, args=[app],
        trigger=IntervalTrigger(hours=1),
        id="hourly_push_check",
        replace_existing=True,
    )

    # Daily at 08:00 UTC — send motivational phrase to all students
    scheduler.add_job(
        func=send_daily_motivation, args=[app],
        trigger=CronTrigger(hour=8, minute=0),
        id="daily_motivation",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("[APScheduler] Scheduler started — hourly activity check + daily 08:00 motivation.")
    return scheduler
