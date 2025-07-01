from marshmallow import Schema, fields, validate

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True) # 모델에 따라 nullable=True 이므로
    start_date = fields.Date(required=True) # 모델 필드명 및 타입 일치
    end_date = fields.Date(required=True)   # 모델 필드명 및 타입 일치
    location = fields.Int(required=True)    # 모델 필드명 및 타입 일치 (Integer)
    created_by = fields.Int(required=True) # 모델에 있지만, 생성 시 자동 할당 또는 dump_only 고려
    external_url = fields.Str(allow_none=True, validate=validate.Length(max=2048))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 