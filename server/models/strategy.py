# ═══════════════════════════════════════════════════════════
# server/models/strategy.py
# WeeklyStrategy — 13-week semester strategy per course & level
# ═══════════════════════════════════════════════════════════

from datetime import datetime
from server.extensions import db


class WeeklyStrategy(db.Model):
    __tablename__ = "weekly_strategies"

    id           = db.Column(db.Integer,     primary_key=True)
    course       = db.Column(db.String(50),  nullable=False)   # programming | database | networking
    level        = db.Column(db.String(10),  nullable=False)   # 100 | 200 | 300
    week         = db.Column(db.Integer,     nullable=False)   # 1-13
    topic        = db.Column(db.String(200), nullable=False)
    activity     = db.Column(db.String(50),  default="lecture") # lecture|lab|assignment|test|project|exam_prep
    strategy     = db.Column(db.Text,        nullable=False)   # regular student strategy
    evening_tip  = db.Column(db.Text,        nullable=True)    # evening-specific addition
    created_by   = db.Column(db.Integer,     db.ForeignKey("users.id"), nullable=True)
    updated_at   = db.Column(db.DateTime,    default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("course", "level", "week", name="uq_course_level_week"),
    )

    def to_dict(self):
        return {
            "id":          self.id,
            "course":      self.course,
            "level":       self.level,
            "week":        self.week,
            "topic":       self.topic,
            "activity":    self.activity,
            "strategy":    self.strategy,
            "evening_tip": self.evening_tip,
            "updated_at":  self.updated_at.isoformat() if self.updated_at else None,
        }
