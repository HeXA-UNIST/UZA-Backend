from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from marshmallow import Schema, fields, validate, ValidationError
from werkzeug.exceptions import HTTPException
import os

app = Flask(__name__)
CORS(app)

# 환경 변수에서 설정을 가져오거나 기본값 사용
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False  # 한글 지원

db = SQLAlchemy(app)

# 스키마 정의
class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    date = fields.DateTime(required=True)
    location = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# 모델 정의
class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat(),
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# 에러 핸들러
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({
        'error': 'Validation Error',
        'messages': error.messages
    }), 400

@app.errorhandler(HTTPException)
def handle_http_error(error):
    return jsonify({
        'error': error.name,
        'message': error.description
    }), error.code

@app.errorhandler(Exception)
def handle_generic_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error)
    }), 500

# API 엔드포인트
@app.route("/api/events", methods=["GET"])
def get_events():
    try:
        events = Event.query.order_by(Event.date.desc()).all()
        return jsonify([event.to_dict() for event in events])
    except Exception as e:
        return handle_generic_error(e)

@app.route("/api/events", methods=["POST"])
def create_event():
    try:
        schema = EventSchema()
        data = schema.load(request.json)
        
        new_event = Event(
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location']
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return jsonify(new_event.to_dict()), 201
    except ValidationError as e:
        return handle_validation_error(e)
    except Exception as e:
        db.session.rollback()
        return handle_generic_error(e)

@app.route("/api/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify(event.to_dict())
    except Exception as e:
        return handle_generic_error(e)

@app.route("/api/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        schema = EventSchema(partial=True)
        data = schema.load(request.json)
        
        for key, value in data.items():
            setattr(event, key, value)
        
        db.session.commit()
        return jsonify(event.to_dict())
    except ValidationError as e:
        return handle_validation_error(e)
    except Exception as e:
        db.session.rollback()
        return handle_generic_error(e)

@app.route("/api/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return handle_generic_error(e)

# 데이터베이스 초기화
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run("0.0.0.0", 8081, debug=True)