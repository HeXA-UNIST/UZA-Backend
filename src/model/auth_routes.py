from flask import Blueprint, request, jsonify
from src.model.auth import Auth, User
from src.middleware import db, mail
from flask_mail import Message
import random, string, datetime

AUTH_EMAIL_DOMAIN = "@unist.ac.kr"
OTP_EXPIRE_MINUTES = 5
OTP_LENGTH = 6

auth_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')

def generate_otp(length=OTP_LENGTH):
    return ''.join(random.choices(string.digits, k=length))

def is_school_email(email):
    return email.lower().endswith(AUTH_EMAIL_DOMAIN)

@auth_bp.route('/request', methods=['POST'])
def request_otp():
    data = request.get_json()
    email = data.get('email')
    nickname = data.get('nickname')
    if not email or not is_school_email(email):
        return jsonify({'message': '학교 이메일(@unist.ac.kr)만 사용 가능합니다.'}), 400
    otp = generate_otp()
    # 기존 인증 정보 삭제(옵션)
    Auth.query.filter_by(email=email).delete()
    db.session.commit()
    # 인증 정보 저장
    auth = Auth(email=email, otp=otp, is_verified=False)
    db.session.add(auth)
    db.session.commit()
    # 이메일 발송
    msg = Message('[UZA] 인증번호 안내', recipients=[email])
    msg.body = f"인증번호: {otp}\n5분 이내에 입력해 주세요."
    mail.send(msg)
    return jsonify({'message': '인증번호가 이메일로 발송되었습니다.'}), 200

@auth_bp.route('/verify', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    nickname = data.get('nickname')
    if not email or not otp:
        return jsonify({'message': '이메일과 인증번호를 모두 입력해 주세요.'}), 400
    auth = Auth.select_by_email(email)
    if not auth or auth.otp != otp:
        return jsonify({'message': '인증번호가 일치하지 않습니다.'}), 400
    # OTP 유효시간 체크
    now = datetime.datetime.now()
    if (now - auth.created_at).total_seconds() > OTP_EXPIRE_MINUTES * 60:
        return jsonify({'message': '인증번호가 만료되었습니다.'}), 400
    # 인증 성공 처리
    auth.update_is_verified(True)
    # 유저가 없으면 회원가입
    user = User.select_by_email(email)
    if not user:
        if not nickname:
            return jsonify({'message': '닉네임이 필요합니다.'}), 400
        if User.select_by_nickname(nickname):
            return jsonify({'message': '이미 사용 중인 닉네임입니다.'}), 400
        user = User(email=email, nickname=nickname)
        db.session.add(user)
        db.session.commit()
    return jsonify({'message': '인증 및 로그인 성공', 'user': {'id': user.id, 'email': user.email, 'nickname': user.nickname}}), 200 