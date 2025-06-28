import React from 'react';

const UsageLimit = ({ usageInfo }) => {
  if (!usageInfo) return null;

  const { usage_count, limit, remaining } = usageInfo;
  const percentage = (usage_count / limit) * 100;
  
  const getUsageFillClass = () => {
    if (percentage >= 100) return 'usage-fill danger';
    if (percentage >= 66) return 'usage-fill warning';
    return 'usage-fill';
  };

  const formatResetTime = (resetTime) => {
    const date = new Date(resetTime);
    return date.toLocaleTimeString('ko-KR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="usage-container">
      <div className="usage-title">
        📊 오늘 사용량
      </div>
      
      <div className="usage-bar">
        <div 
          className="usage-fill"
          style={{ width: `${Math.min(percentage, 100)}%` }}
        ></div>
      </div>
      
      <div className="usage-text">
        {usage_count}/{limit} 회 사용 ({remaining}회 남음)
      </div>
      
      {usageInfo.reset_time && (
        <div className="usage-text" style={{ fontSize: '10px', marginTop: '4px' }}>
          리셋: 내일 {formatResetTime(usageInfo.reset_time)}
        </div>
      )}
    </div>
  );
};

export default UsageLimit; 