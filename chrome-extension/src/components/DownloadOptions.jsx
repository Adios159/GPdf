import React, { useState } from 'react';
import { convertDocument, downloadFile } from '../services/api';

const DownloadOptions = ({ summaryText, sessionId }) => {
  const [selectedFormat, setSelectedFormat] = useState('docx');
  const [isConverting, setIsConverting] = useState(false);

  const formats = [
    { value: 'docx', label: 'DOCX', icon: '📄' },
    { value: 'pdf', label: 'PDF', icon: '📕' },
    { value: 'txt', label: 'TXT', icon: '📝' }
  ];

  const handleDownload = async () => {
    if (!summaryText || !sessionId) {
      alert('요약 텍스트가 없습니다.');
      return;
    }

    setIsConverting(true);
    
    try {
      // 1. 문서 변환 요청
      const result = await convertDocument(summaryText, selectedFormat, sessionId);
      
      // 2. 파일 다운로드
      downloadFile(result.download_url, result.filename);
      
      // 성공 메시지
      alert(`${selectedFormat.toUpperCase()} 파일이 다운로드되었습니다.\n파일명: ${result.filename}`);
      
    } catch (error) {
      console.error('다운로드 실패:', error);
      alert(`다운로드 실패: ${error.message}`);
    } finally {
      setIsConverting(false);
    }
  };

  return (
    <div className="download-container">
      <div className="summary-title">💾 다운로드</div>
      
      <div className="format-options">
        {formats.map((format) => (
          <button
            key={format.value}
            className={`format-btn ${selectedFormat === format.value ? 'selected' : ''}`}
            onClick={() => setSelectedFormat(format.value)}
            disabled={isConverting}
          >
            <div>{format.icon}</div>
            <div>{format.label}</div>
          </button>
        ))}
      </div>
      
      <button 
        className="btn btn-primary btn-full"
        onClick={handleDownload}
        disabled={isConverting || !summaryText}
      >
        {isConverting ? '변환 중...' : `${selectedFormat.toUpperCase()} 다운로드`}
      </button>
    </div>
  );
};

export default DownloadOptions; 