import React, { useState } from 'react';
import { askQuestion } from '../services/api';
import './PDFQAChat.css';

const PDFQAChat = ({ fileId }) => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const validateQuestion = (text) => {
    if (!text || text.trim().length === 0) {
      return { isValid: false, error: '질문을 입력해주세요.' };
    }
    
    if (text.length > 500) {
      return { isValid: false, error: '질문이 너무 깁니다. (최대 500자)' };
    }

    // 프롬프트 인젝션 시도 탐지
    const suspiciousPatterns = [
      /system:/i,
      /assistant:/i,
      /user:/i,
      /ignore previous/i,
      /ignore above/i,
      /forget/i,
      /new prompt/i,
      /{.*}/,  // JSON 형식
      /<.*>/,  // XML/HTML 태그
    ];

    for (const pattern of suspiciousPatterns) {
      if (pattern.test(text)) {
        return { isValid: false, error: '유효하지 않은 입력입니다.' };
      }
    }

    return { isValid: true, error: '' };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // 입력 검증
    const validation = validateQuestion(question);
    if (!validation.isValid) {
      setError(validation.error);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await askQuestion(fileId, question);
      setAnswer(response.answer);
    } catch (err) {
      setError('질문에 답변하는 중 오류가 발생했습니다.');
      console.error('Q&A 오류:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pdf-qa-chat">
      <h3>PDF Q&A</h3>
      
      <form onSubmit={handleSubmit} className="qa-form">
        <input
          type="text"
          value={question}
          onChange={(e) => {
            setQuestion(e.target.value);
            setError(''); // 입력이 변경되면 에러 메시지 초기화
          }}
          placeholder="PDF 내용에 대해 질문해보세요..."
          disabled={loading}
          className="qa-input"
          maxLength={500} // 최대 입력 길이 제한
        />
        <button type="submit" disabled={loading} className="qa-submit">
          {loading ? '답변 중...' : '질문하기'}
        </button>
      </form>

      {error && <div className="qa-error">{error}</div>}
      
      {answer && (
        <div className="qa-answer">
          <h4>답변:</h4>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default PDFQAChat; 