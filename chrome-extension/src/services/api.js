import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// API 클라이언트 설정
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30초 타임아웃
});

// PDF 요약 요청
export const summarizePDF = async (file, sessionId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('session_id', sessionId);

  try {
    const response = await apiClient.post('/pdf/summarize', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || '요약 생성에 실패했습니다.');
  }
};

// 문서 변환 요청
export const convertDocument = async (summaryText, format, sessionId) => {
  try {
    const formData = new FormData();
    formData.append('summary_text', summaryText);
    formData.append('format', format);
    formData.append('session_id', sessionId);

    const response = await apiClient.post('/pdf/convert', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || '문서 변환에 실패했습니다.');
  }
};

// 사용량 확인
export const checkUsage = async (sessionId) => {
  try {
    const response = await apiClient.get(`/pdf/usage/${sessionId}`);
    return response.data;
  } catch (error) {
    // 사용량 정보가 없는 경우 기본값 반환
    return {
      usage_count: 0,
      limit: 3,
      remaining: 3,
      reset_time: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    };
  }
};

// 파일 다운로드
export const downloadFile = (downloadUrl, filename) => {
  const link = document.createElement('a');
  link.href = `${API_BASE_URL}${downloadUrl}`;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// 헬스체크
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health/');
    return response.data;
  } catch (error) {
    throw new Error('서버 연결에 실패했습니다.');
  }
}; 