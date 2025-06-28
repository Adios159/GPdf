# GPdf - PDF 요약 크롬 익스텐션

PDF 파일을 업로드하고 GPT-3.5를 활용하여 요약하는 크롬 익스텐션입니다.

## ✅ 현재 상태 (2024년 6월 28일)

- ✅ **백엔드 서버 정상 실행 중** (http://127.0.0.1:8000)
- ✅ **PDF 요약 기능 완전 작동**
- ✅ **파일 다운로드 기능 정상화**
- ✅ **한글 폰트 문제 해결** (모든 출력 형식)
- 🔄 Chrome Extension 연동 테스트 진행 중

## 🚀 기능

- PDF 파일 업로드 (5MB 이하)
- 첫 3페이지 텍스트 추출 및 요약
- 결과를 docx/pdf/txt 형식으로 다운로드
- 하루 3회 사용 제한 (세션 기반)

## 📁 프로젝트 구조

```
GPdf/
├── chrome-extension/     # 크롬 익스텐션 (React)
├── backend/             # FastAPI 백엔드
└── README.md
```

## 🛠️ 기술 스택

### 프론트엔드
- React
- Chrome Extension Manifest v3
- Webpack

### 백엔드
- FastAPI
- PyMuPDF (PDF 처리)
- OpenAI GPT-3.5 API
- python-docx, pdfkit (문서 변환)

## 🚀 실행 방법

### 백엔드 실행 (현재 실행 중 ✅)
```bash
cd backend
pip install -r requirements.txt

# 개발 모드로 실행 (권장)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**서버 접속**: http://127.0.0.1:8000
- API 문서: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### 크롬 익스텐션 빌드
```bash
cd chrome-extension
npm install
npm run build

# 개발 모드
npm run dev
```

## 🔧 최근 해결한 주요 문제들

### 1. 파일 다운로드 URL 중복 문제 ✅
- **문제**: API URL이 중복되어 404 에러 발생
- **해결**: 상대 경로 사용으로 URL 정상화

### 2. 한글 폰트 깨짐 문제 ✅  
- **문제**: PDF, DOCX 파일에서 한글이 깨져서 출력
- **해결**: 시스템 한글 폰트 자동 감지 및 적용

### 3. 서버 안정성 향상 ✅
- CORS 설정으로 크로스 오리진 요청 허용
- 자동 리로드로 개발 효율성 증대

## 📝 라이센스

MIT License 