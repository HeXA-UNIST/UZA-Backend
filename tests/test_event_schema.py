import pytest
from src.model.event_schemas import EventSchema
from marshmallow import ValidationError

def test_event_schema_valid():
    valid_data = {
        'title': '테스트 이벤트',
        'description': '설명',
        'start_date': '2025-01-01',
        'end_date': '2025-01-02',
        'location': 1,
        'created_by': 123,
        'external_url': 'https://example.com'
    }
    schema = EventSchema()
    result = schema.load(valid_data)
    assert result['title'] == '테스트 이벤트'
    assert result['location'] == 1


def test_event_schema_missing_required():
    invalid_data = {
        'description': '설명',
        'start_date': '2025-01-01',
        'end_date': '2025-01-02',
        'location': 1,
        'created_by': 123
    }
    schema = EventSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_data)
    assert 'title' in excinfo.value.messages


def test_event_schema_invalid_length():
    invalid_data = {
        'title': '',  # 최소 길이 위반
        'description': '설명',
        'start_date': '2025-01-01',
        'end_date': '2025-01-02',
        'location': 1,
        'created_by': 123
    }
    schema = EventSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_data)
    assert 'title' in excinfo.value.messages 