import React, { useState } from 'react';
import { summarizePDF } from '../services/api';

const FileUpload = ({ sessionId, onUploadStart, onUploadSuccess, onUploadError, usageInfo }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleFileSelect = async (file) => {
    if (!file) return;
    
    // 파일 검증
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      onUploadError('PDF 파일만 업로드 가능합니다.');
      return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
      onUploadError('파일 크기가 5MB를 초과합니다.');
      return;
    }
    
    if (!sessionId) {
      onUploadError('세션 ID가 없습니다. 페이지를 새로고침해주세요.');
      return;
    }
    
    // 업로드 시작
    onUploadStart();
    
    try {
      // 실제 API 호출
      const result = await summarizePDF(file, sessionId);
      
      onUploadSuccess({
        summary: result.summary,
        page_count: result.page_count,
        usage_remaining: result.usage_remaining,
        processing_time: result.processing_time
      });
      
    } catch (error) {
      console.error('PDF 요약 실패:', error);
      onUploadError(error.message || '요약 생성 중 오류가 발생했습니다.');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  if (!usageInfo || usageInfo.remaining <= 0) {
    return (
      <div className="error-container">
        <div className="error-icon">🚫</div>
        <h3>사용 한도 초과</h3>
        <p className="error-message">오늘의 사용 한도를 모두 사용했습니다. 내일 다시 시도해주세요.</p>
      </div>
    );
  }

  return (
    <div 
      className={`upload-area ${isDragging ? 'dragover' : ''}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      <div className="upload-icon">📄</div>
      <div className="upload-text">PDF 파일을 드래그하거나 클릭하여 업로드</div>
      <div className="upload-hint">최대 5MB, 첫 3페이지 요약</div>
      
      <input 
        type="file" 
        accept=".pdf" 
        style={{ display: 'none' }}
        id="file-input"
        onChange={(e) => handleFileSelect(e.target.files[0])}
      />
      <label htmlFor="file-input" className="btn btn-primary">
        파일 선택
      </label>
    </div>
  );
};

export default FileUpload; 