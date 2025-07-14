import pytest
from src.model.auth import Auth, User
from src.middleware import create_app, db as _db, mail as _mail
from flask import Flask
from flask_mail import Message

TEST_EMAIL = "test@unist.ac.kr"
TEST_NICKNAME = "testuser"

@pytest.fixture(scope="module")
def app():
    from config import Config
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        MAIL_SUPPRESS_SEND = True
        MAIL_DEFAULT_SENDER = "noreply@unist.ac.kr"
        SESSION_TYPE = "filesystem"
    app, _ = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clear_auth_user():
    # 각 테스트 전후로 인증/유저 데이터 정리
    yield
    Auth.query.delete()
    User.query.delete()
    _db.session.commit()

def test_email_otp_signup_and_login(client):
    # 1. OTP 요청
    resp = client.post("/api/auth/request", json={"email": TEST_EMAIL, "nickname": TEST_NICKNAME})
    assert resp.status_code == 200
    # 2. DB에서 OTP 직접 조회
    otp = Auth.query.filter_by(email=TEST_EMAIL).first().otp
    assert otp is not None
    # 3. OTP 인증(회원가입)
    resp2 = client.post("/api/auth/verify", json={"email": TEST_EMAIL, "otp": otp, "nickname": TEST_NICKNAME})
    assert resp2.status_code == 200
    data = resp2.get_json()
    assert data["user"]["email"] == TEST_EMAIL
    assert data["user"]["nickname"] == TEST_NICKNAME
    # 4. 이미 가입된 유저로 로그인(OTP 재요청)
    resp3 = client.post("/api/auth/request", json={"email": TEST_EMAIL})
    assert resp3.status_code == 200
    otp2 = Auth.query.filter_by(email=TEST_EMAIL).first().otp
    resp4 = client.post("/api/auth/verify", json={"email": TEST_EMAIL, "otp": otp2})
    assert resp4.status_code == 200
    data2 = resp4.get_json()
    assert data2["user"]["email"] == TEST_EMAIL 