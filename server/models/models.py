# ═══════════════════════════════════════════════════════════
# server/models/models.py
# All SQLAlchemy database models for UPSA ITM Chatbot
# ═══════════════════════════════════════════════════════════

from datetime import datetime
from server.extensions import db


# ─── User ──────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer,     primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20),  nullable=False)
    level         = db.Column(db.String(10),  nullable=True)
    semester      = db.Column(db.String(5),   nullable=True)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    messages = db.relationship(
        "ChatMessage", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id":       self.id,
            "name":     self.name,
            "email":    self.email,
            "role":     self.role,
            "level":    self.level,
            "semester": self.semester,
        }


# ─── Chat Message ───────────────────────────────────────────
class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id         = db.Column(db.Integer,    primary_key=True)
    user_id    = db.Column(db.Integer,    db.ForeignKey("users.id"), nullable=False)
    role       = db.Column(db.String(20), nullable=False)
    content    = db.Column(db.Text,       nullable=False)
    intent     = db.Column(db.String(80), nullable=True)
    confidence = db.Column(db.Float,      nullable=True)
    fallback   = db.Column(db.Boolean,    default=False)
    timestamp  = db.Column(db.DateTime,   default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "role":       self.role,
            "content":    self.content,
            "intent":     self.intent,
            "confidence": self.confidence,
            "fallback":   self.fallback,
            "timestamp":  self.timestamp.isoformat(),
        }


# ─── Knowledge Base ─────────────────────────────────────────
class KnowledgeBase(db.Model):
    __tablename__ = "knowledge_base"

    id            = db.Column(db.Integer,      primary_key=True)
    intent_name   = db.Column(db.String(100),  unique=True, nullable=False)
    keywords      = db.Column(db.Text,         nullable=False)
    response_text = db.Column(db.Text,         nullable=False)
    level         = db.Column(db.String(10),   default="all")
    created_by    = db.Column(db.Integer,      db.ForeignKey("users.id"), nullable=True)
    updated_at    = db.Column(db.DateTime,     default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":            self.id,
            "intent_name":   self.intent_name,
            "keywords":      [k.strip() for k in self.keywords.split(",") if k.strip()],
            "response_text": self.response_text,
            "level":         self.level,
            "updated_at":    self.updated_at.isoformat() if self.updated_at else None,
        }


# ─── Reminder ───────────────────────────────────────────────
class Reminder(db.Model):
    __tablename__ = "reminders"

    id          = db.Column(db.Integer,     primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=True)
    date        = db.Column(db.Date,        nullable=False)
    time        = db.Column(db.String(5),   nullable=True)   # "HH:MM" — exact time of activity
    level       = db.Column(db.String(10),  default="all")
    semester    = db.Column(db.String(5),   default="1")
    week        = db.Column(db.Integer,     nullable=True)   # semester week number 1–12
    type        = db.Column(db.String(30),  default="assignment")
    created_by  = db.Column(db.Integer,     db.ForeignKey("users.id"), nullable=True)
    created_at  = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "date":        self.date.isoformat(),
            "time":        self.time or "08:00",
            "level":       self.level,
            "semester":    self.semester,
            "week":        self.week,
            "type":        self.type,
        }


# ─── Unanswered Query Log ───────────────────────────────────
class UnansweredQuery(db.Model):
    __tablename__ = "unanswered_queries"

    id            = db.Column(db.Integer,    primary_key=True)
    question      = db.Column(db.Text,       nullable=False)
    student_level = db.Column(db.String(10), nullable=True)
    user_id       = db.Column(db.Integer,    db.ForeignKey("users.id"), nullable=True)
    date          = db.Column(db.DateTime,   default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":            self.id,
            "question":      self.question,
            "student_level": self.student_level,
            "date":          self.date.isoformat(),
        }


# ─── Intent Log ─────────────────────────────────────────────
class IntentLog(db.Model):
    __tablename__ = "intent_logs"

    id          = db.Column(db.Integer,     primary_key=True)
    intent_name = db.Column(db.String(100), nullable=False)
    user_id     = db.Column(db.Integer,     db.ForeignKey("users.id"), nullable=True)
    user_level  = db.Column(db.String(10),  nullable=True)
    timestamp   = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "intent_name": self.intent_name,
            "user_level":  self.user_level,
            "timestamp":   self.timestamp.isoformat(),
        }


# ─── Motivational Messages ──────────────────────────────────
class Motivation(db.Model):
    __tablename__ = "motivations"

    id      = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text,    nullable=False)

    def to_dict(self):
        return {"id": self.id, "message": self.message}


# ─── Push Subscription ──────────────────────────────────────
class PushSubscription(db.Model):
    __tablename__ = "push_subscriptions"

    id         = db.Column(db.Integer,  primary_key=True)
    user_id    = db.Column(db.Integer,  db.ForeignKey("users.id"), nullable=False)
    endpoint   = db.Column(db.Text,     nullable=False, unique=True)
    p256dh     = db.Column(db.Text,     nullable=False)
    auth       = db.Column(db.Text,     nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        "User", backref=db.backref("push_subscriptions", lazy=True)
    )

    def to_dict(self):
        return {
            "id":       self.id,
            "endpoint": self.endpoint,
            "p256dh":   self.p256dh,
            "auth":     self.auth,
        }

    def to_webpush_sub(self):
        """Return dict compatible with pywebpush subscription_info argument."""
        return {
            "endpoint": self.endpoint,
            "keys": {
                "p256dh": self.p256dh,
                "auth":   self.auth,
            },
        }
