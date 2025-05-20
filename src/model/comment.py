from datetime import datetime
from typing import List

from src.middleware import db

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, index=True)
    event_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now)

    def create(self, user_id: int, nickname: str, event_id: str, content: str) -> "Comment":
        self.user_id = user_id
        self.nickname = nickname
        self.event_id = event_id
        self.content = content
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def select_by_event_id(cls, event_id: int, limit: int = 1000) -> List["Comment"]:
        return cls.query.filter(cls.event_id == event_id).order_by(cls.created_at.desc()).limit(limit).all()

    @classmethod
    def delete_by_id(cls, comment_id: int) -> bool:
        comment = cls.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True
        return False
    
    def as_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }