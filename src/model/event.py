from datetime import datetime
from typing import List

from src.middleware import db

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    external_url = db.Column(db.String(2048), nullable=True)


    def create(self, title: str, description: str, start_date: datetime.date, end_date: datetime.date,
               location: int, created_by: int, external_url: str = None) -> "Event":
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.created_by = created_by
        self.external_url = external_url
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def select_by_event_id(cls, event_id: str, limit: int = 1000) -> List["Event"]:
        return cls.query.filter(cls.event_id == event_id).order_by(cls.created_at.desc()).limit(limit).all()

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "location": self.location,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "external_url": self.external_url
        }

class EventSchedule(db.Model):
    __tablename__ = "event_schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=True)

    def create(self, event_id: int, start_date: datetime, end_date: datetime, content: str = None) -> "EventSchedule":
        self.event_id = event_id
        self.start_date = start_date
        self.end_date = end_date
        self.content = content
        db.session.add(self)
        db.session.commit()
        return self

    def as_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "content": self.content
        }