// Chrome Extension Background Script (Service Worker)

// 익스텐션 설치 시 실행
chrome.runtime.onInstalled.addListener(() => {
  console.log('GPdf Extension installed');
  
  // 초기 설정
  chrome.storage.local.set({
    installDate: Date.now(),
    version: '1.0.0'
  });
});

// 익스텐션 시작 시 실행
chrome.runtime.onStartup.addListener(() => {
  console.log('GPdf Extension started');
});

// 메시지 리스너 (팝업과 통신)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getSessionInfo') {
    // 세션 정보 반환
    chrome.storage.local.get(['sessionId', 'sessionDate'], (result) => {
      sendResponse(result);
    });
    return true; // 비동기 응답을 위해 true 반환
  }
  
  if (request.action === 'downloadFile') {
    // 파일 다운로드 처리
    chrome.downloads.download({
      url: request.url,
      filename: request.filename
    }, (downloadId) => {
      sendResponse({ downloadId });
    });
    return true;
  }
});

// 알람 설정 (일일 사용량 리셋용)
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'resetDailyUsage') {
    // 일일 사용량 리셋
    chrome.storage.local.remove(['sessionId', 'sessionDate', 'usageInfo']);
    console.log('Daily usage reset');
  }
});

// 매일 자정에 사용량 리셋 알람 설정
const setupDailyReset = () => {
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);
  tomorrow.setHours(0, 0, 0, 0);
  
  chrome.alarms.create('resetDailyUsage', {
    when: tomorrow.getTime(),
    periodInMinutes: 24 * 60 // 24시간마다 반복
  });
};

// 알람 설정 실행
setupDailyReset(); 