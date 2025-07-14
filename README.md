# 학교 행사 알리미 백엔드

이 프로젝트는 학교 행사를 관리하고 API를 통해 제공하는 Flask 기반의 백엔드 서비스입니다.

## 주요 기능

- 행사 CRUD (생성, 조회, 수정, 삭제) API 제공
- 데이터 유효성 검사
- 표준화된 에러 처리

## 설치 및 실행 방법

1.  **저장소 복제:**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **가상 환경 생성 및 활성화:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate  # Windows
    ```

3.  **필수 패키지 설치:**
    ```bash
    pip3 install -r requirements.txt
    ```

4.  **애플리케이션 실행:**
    ```bash
    python3 app.py
    ```
    애플리케이션은 기본적으로 `http://localhost:8081` 에서 실행됩니다.

## 테스트 실행

1. **pytest 설치** (한 번만 실행)
    ```bash
    pip install pytest
    ```

2. **테스트 실행** (프로젝트 루트에서)
    ```bash
    PYTHONPATH=. pytest
    ```

- 테스트 코드는 `tests/` 폴더에 위치합니다.
- 테스트에는 이벤트 스키마, **이메일 인증(OTP) 및 로그인** 기능도 포함됩니다.
- 테스트가 모두 통과하면 `... [100%]` 메시지가 출력됩니다.
- 경고(Warning)는 무시해도 무방합니다.

### 이메일 인증(OTP) 및 로그인 테스트 방법

- 인증 관련 테스트는 `tests/test_auth.py` 파일에 있습니다.
- 아래 명령어로 인증(OTP 발송/검증, 회원가입/로그인) 플로우를 자동으로 검증할 수 있습니다.

    ```bash
    PYTHONPATH=. pytest tests/test_auth.py
    ```

- 테스트는 실제 메일 발송 없이(테스트 환경에서 suppress) 동작합니다.
- 테스트가 통과하면 인증 API가 정상적으로 동작함을 의미합니다.

## API 엔드포인트

- `GET /api/events`: 모든 행사 목록 조회
- `POST /api/events`: 새로운 행사 생성
- `GET /api/events/<event_id>`: 특정 행사 상세 조회
- `PUT /api/events/<event_id>`: 특정 행사 정보 수정
- `DELETE /api/events/<event_id>`: 특정 행사 삭제

### 예시: 새로운 행사 생성

```bash
curl -X POST http://localhost:8081/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "신입생 환영회",
    "description": "2025학년도 신입생들을 위한 환영 행사입니다.",
    "date": "2025-03-05T18:00:00",
    "location": "학생회관"
  }'
``` 