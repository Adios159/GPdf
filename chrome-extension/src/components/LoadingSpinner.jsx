import React from 'react';

const LoadingSpinner = ({ message = "처리 중..." }) => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <div className="loading-text">{message}</div>
    </div>
  );
};

export default LoadingSpinner; 