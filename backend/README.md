# GPdf Backend API

PDF 요약 서비스의 FastAPI 백엔드입니다.

## ✅ 현재 상태 (2024년 6월 28일 업데이트)

- ✅ 서버 정상 실행 중 (http://127.0.0.1:8000)
- ✅ PDF 요약 기능 정상 작동
- ✅ 파일 다운로드 URL 중복 문제 해결
- ✅ 한글 폰트 깨짐 문제 해결 (PDF, DOCX 포함)
- ✅ 모든 문서 변환 형식 지원 (PDF, DOCX, TXT)

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```
OPENAI_API_KEY=your_openai_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### 3. 서버 실행

```bash
# 개발 모드 (권장)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# 또는 간단한 실행
uvicorn app.main:app --reload
```

서버가 http://127.0.0.1:8000 에서 실행됩니다.

**현재 실행 상태**: ✅ 서버 정상 실행 중

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health Check: http://127.0.0.1:8000/health
- Root Endpoint: http://127.0.0.1:8000/

## 🧪 테스트 방법

### 1. 서버 상태 확인
```bash
curl http://127.0.0.1:8000/health
```

### 2. Chrome Extension과 연동
- Chrome Extension을 설치하여 PDF 요약 기능을 테스트할 수 있습니다.
- API Base URL: `http://localhost:8000/api/v1`

### 3. 지원되는 파일 형식
- **입력**: PDF 파일만 지원
- **출력**: PDF, DOCX, TXT 형식으로 변환 가능

## 🛠️ 주요 기능

- PDF 파일 업로드 및 텍스트 추출
- GPT-3.5를 이용한 요약 생성
- 다양한 형식(docx, pdf, txt)으로 결과 변환
- 세션 기반 사용량 제한 (하루 3회)
- 한글 폰트 자동 감지 및 적용
- CORS 설정으로 Chrome Extension 연동

## 🔧 최근 해결한 문제들

### 1. 파일 다운로드 URL 중복 문제 (해결됨)
**문제**: `/api/v1/api/v1/pdf/download/...` 형태로 URL이 중복되어 404 에러 발생
**해결**: PDF 엔드포인트에서 상대 경로 `/pdf/download/{filename}` 반환하도록 수정

### 2. 한글 폰트 깨짐 문제 (해결됨)
**문제**: PDF 및 DOCX 파일에서 한글이 깨져서 표시됨
**해결**: 
- 시스템 한글 폰트 자동 감지 (NanumGothic, 맑은고딕 등)
- ReportLab에 한글 폰트 등록
- DOCX에서 한글 폰트 명시적 설정
- UTF-8 인코딩으로 텍스트 파일 처리

### 3. 서버 실행 최적화
- uvicorn 설정으로 개발 모드 실행
- reload 옵션으로 코드 변경 자동 감지
- CORS 미들웨어로 크로스 오리진 요청 허용

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── api/v1/endpoints/    # API 엔드포인트
│   ├── core/               # 핵심 비즈니스 로직
│   ├── models/             # Pydantic 모델
│   ├── utils/              # 유틸리티 함수
│   ├── config.py           # 설정 관리
│   └── main.py             # FastAPI 앱 엔트리
├── downloads/              # 변환된 파일 저장소
├── requirements.txt        # 파이썬 패키지 목록
└── README.md
``` 