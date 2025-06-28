# GPdf Chrome Extension

PDF 파일을 업로드하고 GPT-3.5를 활용하여 요약하는 크롬 익스텐션입니다.

## 🚀 기능

- PDF 파일 드래그 앤 드롭 업로드
- 첫 3페이지 자동 텍스트 추출
- GPT-3.5 기반 한국어 요약 생성
- 다양한 형식(DOCX, PDF, TXT) 다운로드
- 하루 3회 사용 제한 (세션 기반)

## 🛠️ 개발 및 빌드

### 1. 의존성 설치

```bash
npm install
```

### 2. 개발 모드 실행

```bash
npm run dev
```

### 3. 프로덕션 빌드

```bash
npm run build
```

빌드된 파일은 `dist/` 폴더에 생성됩니다.

### 4. 크롬에 익스텐션 로드

1. Chrome 브라우저에서 `chrome://extensions/` 접속
2. "개발자 모드" 활성화
3. "압축해제된 확장 프로그램을 로드합니다" 클릭
4. `dist/` 폴더 선택

## 📁 프로젝트 구조

```
chrome-extension/
├── public/
│   ├── popup.html          # 팝업 HTML
│   └── icons/              # 아이콘 파일들
├── src/
│   ├── popup/              # 팝업 관련
│   │   ├── App.jsx         # 메인 앱 컴포넌트
│   │   ├── index.js        # 엔트리 포인트
│   │   └── popup.css       # 팝업 스타일
│   ├── components/         # React 컴포넌트
│   │   ├── FileUpload.jsx  # 파일 업로드
│   │   └── LoadingSpinner.jsx # 로딩 스피너
│   ├── services/           # API 및 스토리지 서비스
│   │   ├── api.js          # API 호출
│   │   └── storage.js      # 로컬 스토리지
│   └── background/         # 백그라운드 스크립트
│       └── background.js   # 서비스 워커
├── manifest.json           # 익스텐션 매니페스트
├── webpack.config.js       # 웹팩 설정
└── package.json
```

## ⚙️ 설정

백엔드 API 서버 주소는 `src/services/api.js`에서 변경할 수 있습니다:

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

## 🔧 요구 사항

- Node.js 16 이상
- Chrome 브라우저
- 백엔드 API 서버 실행 필요

## 📝 라이센스

MIT License 