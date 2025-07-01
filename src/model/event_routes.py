from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from src.middleware import db
from .event import Event # 기존 Event 모델
from .event_schemas import EventSchema # 새로 만든 스키마

event_schema = EventSchema()
events_schema = EventSchema(many=True)

event_bp = Blueprint('event_api', __name__, url_prefix='/api/events')

# Blueprint 에러 핸들러 (필요에 따라 추가 또는 공통 에러 핸들러 사용)
@event_bp.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.messages), 400

@event_bp.route('/', methods=['GET'])
def get_events_route(): # 함수 이름 변경 (get_events -> get_events_route)
    try:
        events = Event.query.order_by(Event.created_at.desc()).all()
        return jsonify(events_schema.dump(events)), 200
    except Exception as e:
        # 공통 에러 핸들러를 사용하거나 여기서 직접 처리
        return jsonify(error=str(e)), 500 

@event_bp.route('/', methods=['POST'])
def create_event_route(): # 함수 이름 변경
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        data = event_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400 # Blueprint 에러 핸들러가 처리할 수도 있음

    # created_by는 실제로는 인증된 사용자 ID여야 함. 여기서는 스키마에 따라 처리.
    # Event 모델의 create 메서드나 직접 생성을 고려.
    new_event = Event(
        title=data['title'], 
        description=data.get('description'),
        start_date=data['start_date'],
        end_date=data['end_date'],
        location=data['location'],
        created_by=data['created_by'], # 스키마에서 required=True로 설정됨
        external_url=data.get('external_url')
    )
    # 또는 new_event = Event().create(...)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(event_schema.dump(new_event)), 201

@event_bp.route('/<int:event_id>/', methods=['GET'])
def get_event_detail_route(event_id): # 함수 이름 변경
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify(event_schema.dump(event)), 200
    except Exception as e:
        return jsonify(error=str(e)), 404 # HTTPException을 공통 핸들러가 처리하도록 할 수도 있음

@event_bp.route('/<int:event_id>/', methods=['PUT'])
def update_event_route(event_id): # 함수 이름 변경
    event = Event.query.get_or_404(event_id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        data = event_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        if hasattr(event, key):
            setattr(event, key, value)
    
    db.session.commit()
    return jsonify(event_schema.dump(event)), 200

@event_bp.route('/<int:event_id>/', methods=['DELETE'])
def delete_event_route(event_id): # 함수 이름 변경
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return '', 204 