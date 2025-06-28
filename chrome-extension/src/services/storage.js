// 크롬 익스텐션 스토리지 API 사용

// 세션 ID 조회
export const getSessionId = async () => {
  try {
    const result = await chrome.storage.local.get(['sessionId', 'sessionDate']);
    const today = new Date().toDateString();
    
    // 오늘 날짜의 세션 ID가 있으면 반환
    if (result.sessionId && result.sessionDate === today) {
      return result.sessionId;
    }
    
    return null;
  } catch (error) {
    console.error('세션 ID 조회 실패:', error);
    return null;
  }
};

// 세션 ID 저장
export const setSessionId = async (sessionId) => {
  try {
    const today = new Date().toDateString();
    await chrome.storage.local.set({
      sessionId: sessionId,
      sessionDate: today
    });
  } catch (error) {
    console.error('세션 ID 저장 실패:', error);
  }
};

// 세션 ID 생성 또는 복원
export const generateSessionId = async () => {
  try {
    // 기존 세션 ID 확인
    const result = await chrome.storage.local.get(['sessionId', 'sessionDate']);
    const today = new Date().toDateString();
    
    // 오늘 날짜의 세션 ID가 있으면 재사용
    if (result.sessionId && result.sessionDate === today) {
      return result.sessionId;
    }
    
    // 새로운 세션 ID 생성
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    // 스토리지에 저장
    await chrome.storage.local.set({
      sessionId: sessionId,
      sessionDate: today
    });
    
    return sessionId;
  } catch (error) {
    console.error('세션 ID 생성 실패:', error);
    // 폴백: 메모리 기반 세션 ID
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
};

// 사용량 정보 저장
export const saveUsageInfo = async (usageInfo) => {
  try {
    await chrome.storage.local.set({
      usageInfo: usageInfo,
      lastUpdated: Date.now()
    });
  } catch (error) {
    console.error('사용량 정보 저장 실패:', error);
  }
};

// 사용량 정보 조회
export const getUsageInfo = async () => {
  try {
    const result = await chrome.storage.local.get(['usageInfo', 'lastUpdated']);
    
    // 데이터가 24시간 이상 오래되었으면 null 반환
    if (result.lastUpdated && Date.now() - result.lastUpdated > 24 * 60 * 60 * 1000) {
      return null;
    }
    
    return result.usageInfo || null;
  } catch (error) {
    console.error('사용량 정보 조회 실패:', error);
    return null;
  }
};

// 앱 설정 저장
export const saveSettings = async (settings) => {
  try {
    await chrome.storage.sync.set({ settings });
  } catch (error) {
    console.error('설정 저장 실패:', error);
  }
};

// 앱 설정 조회
export const getSettings = async () => {
  try {
    const result = await chrome.storage.sync.get(['settings']);
    return result.settings || {};
  } catch (error) {
    console.error('설정 조회 실패:', error);
    return {};
  }
}; 