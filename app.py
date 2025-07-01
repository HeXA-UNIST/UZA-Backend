import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.middleware import create_app # src.middleware에서 create_app 가져오기
from config import Config # 루트의 config.py에서 Config 가져오기
from src.model.event_routes import event_bp # 새로 만든 Event Blueprint 가져오기

# 환경 변수에서 FLASK_CONFIG를 가져오거나 기본값으로 "development" 사용
config_name = os.getenv('FLASK_CONFIG', 'development')
config_obj = Config.get_config(config_name) 

app, socketio = create_app(config_obj) # create_app 호출

# Event Blueprint 등록 (create_app 내부에서 할 수도 있지만, 여기서 명시적으로 등록)
app.register_blueprint(event_bp)

# # 데이터베이스 초기화는 create_app 내부에서 처리됨
# with app.app_context():
#     db.create_all() # 이미 create_app에 있음

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8081, debug=app.config.get('DEBUG', True))