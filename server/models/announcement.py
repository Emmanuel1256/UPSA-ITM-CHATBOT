# ═══════════════════════════════════════════════════════════
# server/models/announcement.py
# Announcement + QueryLog models
# ═══════════════════════════════════════════════════════════

from datetime import datetime
from server.extensions import db


# ─── Announcements ──────────────────────────────────────────
class Announcement(db.Model):
    __tablename__ = "announcements"

    id         = db.Column(db.Integer,    primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    body       = db.Column(db.Text,        nullable=False)
    author_id  = db.Column(db.Integer,    db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime,   default=datetime.utcnow)
    active     = db.Column(db.Boolean,    default=True)

    author = db.relationship("User", backref=db.backref("announcements", lazy=True))

    def to_dict(self):
        return {
            "id":         self.id,
            "title":      self.title,
            "body":       self.body,
            "author":     self.author.name if self.author else "Unknown",
            "created_at": self.created_at.isoformat(),
            "active":     self.active,
        }


# ─── Query Log (for insights) ───────────────────────────────
class QueryLog(db.Model):
    __tablename__ = "query_log"

    id         = db.Column(db.Integer,    primary_key=True)
    query_text = db.Column(db.Text,       nullable=False)
    intent     = db.Column(db.String(100), nullable=True)
    confidence = db.Column(db.Float,      nullable=True)
    fallback   = db.Column(db.Boolean,    default=False)
    user_level = db.Column(db.String(10), nullable=True)
    timestamp  = db.Column(db.DateTime,   default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "query_text": self.query_text,
            "intent":     self.intent,
            "confidence": self.confidence,
            "fallback":   self.fallback,
            "user_level": self.user_level,
            "timestamp":  self.timestamp.isoformat(),
        }
