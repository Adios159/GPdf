import React, { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import SummaryResult from '../components/SummaryResult';
import DownloadOptions from '../components/DownloadOptions';
import UsageLimit from '../components/UsageLimit';
import { checkUsage, healthCheck } from '../services/api';
import { getSessionId, setSessionId } from '../services/storage';
import PDFQAChat from '../components/PDFQAChat';
import './popup.css';

const App = () => {
  const [sessionId, setCurrentSessionId] = useState(null);
  const [usageInfo, setUsageInfo] = useState(null);
  const [currentStep, setCurrentStep] = useState('upload'); // upload, loading, summary, download
  const [summaryData, setSummaryData] = useState(null);
  const [error, setError] = useState(null);
  const [serverStatus, setServerStatus] = useState('checking'); // checking, online, offline
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState('');
  const [fileId, setFileId] = useState('');

  // 초기화
  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // 1. 서버 상태 확인
      await healthCheck();
      setServerStatus('online');

      // 2. 세션 ID 설정
      let currentSessionId = await getSessionId();
      if (!currentSessionId) {
        currentSessionId = generateSessionId();
        await setSessionId(currentSessionId);
      }
      setCurrentSessionId(currentSessionId);

      // 3. 사용량 정보 로드
      const usage = await checkUsage(currentSessionId);
      setUsageInfo(usage);

    } catch (error) {
      console.error('앱 초기화 실패:', error);
      setServerStatus('offline');
      setError('서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.');
    }
  };

  const generateSessionId = () => {
    return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
  };

  const handleUploadStart = () => {
    setCurrentStep('loading');
    setError(null);
  };

  const handleUploadSuccess = (data) => {
    setSummary(data.summary);
    setFileId(data.file_id);
    setError('');
  };

  const handleUploadError = (err) => {
    setError(err.message);
    setSummary('');
    setFileId('');
  };

  const handleNewUpload = () => {
    setCurrentStep('upload');
    setSummaryData(null);
    setError(null);
  };

  // 서버 오프라인 상태
  if (serverStatus === 'offline') {
    return (
      <div className="app">
        <header className="app-header">
          <h1>📄 GPdf</h1>
          <p>PDF 요약 도구</p>
        </header>
        
        <main className="app-main">
          <div className="error-container">
            <div className="error-icon">🔌</div>
            <h3>서버 연결 실패</h3>
            <p className="error-message">{error}</p>
            <button className="btn btn-secondary" onClick={initializeApp}>
              다시 시도
            </button>
          </div>
        </main>
        
        <footer className="app-footer">
          <small>Powered by GPT-3.5 Turbo</small>
        </footer>
      </div>
    );
  }

  // 로딩 상태
  if (serverStatus === 'checking' || !sessionId) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>📄 GPdf</h1>
          <p>PDF 요약 도구</p>
        </header>
        
        <main className="app-main">
          <LoadingSpinner message="초기화 중..." />
        </main>
        
        <footer className="app-footer">
          <small>Powered by GPT-3.5 Turbo</small>
        </footer>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📄 GPdf</h1>
        <p>PDF 요약 도구</p>
      </header>
      
      <main className="app-main">
        {/* 사용량 표시 */}
        {usageInfo && (
          <UsageLimit usageInfo={usageInfo} />
        )}

        {/* 에러 메시지 */}
        {error && (
          <div className="error-container">
            <div className="error-icon">⚠️</div>
            <p className="error-message">{error}</p>
          </div>
        )}

        {/* 단계별 컴포넌트 렌더링 */}
        {currentStep === 'upload' && (
          <FileUpload
            sessionId={sessionId}
            onUploadStart={handleUploadStart}
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
            onUploadEnd={() => setLoading(false)}
            usageInfo={usageInfo}
          />
        )}

        {currentStep === 'loading' && (
          <LoadingSpinner message="PDF를 분석하고 요약을 생성하는 중..." />
        )}

        {currentStep === 'summary' && summaryData && (
          <>
            <SummaryResult 
              summary={summaryData.summary}
              pageCount={summaryData.page_count}
              processingTime={summaryData.processing_time}
              onNewUpload={handleNewUpload}
            />
            <DownloadOptions
              summaryText={summaryData.summary}
              sessionId={sessionId}
            />
          </>
        )}

        {fileId && <PDFQAChat fileId={fileId} />}
      </main>
      
      <footer className="app-footer">
        <small>Powered by GPT-3.5 Turbo</small>
      </footer>
    </div>
  );
};

export default App; 