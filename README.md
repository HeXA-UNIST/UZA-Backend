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