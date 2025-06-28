import React from 'react';

const SummaryResult = ({ summary, pageCount = 3 }) => {
  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(summary).then(() => {
      // 간단한 피드백 (실제로는 토스트 메시지 등으로 개선 가능)
      alert('클립보드에 복사되었습니다!');
    }).catch(() => {
      alert('복사에 실패했습니다.');
    });
  };

  return (
    <div className="summary-container">
      <div className="summary-title">
        📄 요약 결과 ({pageCount}페이지)
      </div>
      
      <div className="summary-content">
        {summary}
      </div>
      
      <button 
        className="btn btn-outline btn-small"
        onClick={handleCopyToClipboard}
        style={{ marginTop: '12px' }}
      >
        📋 복사하기
      </button>
    </div>
  );
};

export default SummaryResult; 