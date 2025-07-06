from openai import OpenAI
from app.config import settings
from app.utils.security import SecurityUtils


class OpenAIClient:
    """OpenAI API 클라이언트 래퍼"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.security = SecurityUtils()
    
    def create_chat_completion(
        self,
        messages: list,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500,
        temperature: float = 0.3
    ):
        """채팅 완성 요청을 생성합니다."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response
        except Exception as e:
            raise ValueError(f"OpenAI API 호출 실패: {str(e)}")
    
    def create_pdf_qa(
        self,
        question: str,
        context: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500,
        temperature: float = 0.3
    ):
        """PDF 내용을 바탕으로 질문에 답변합니다."""
        try:
            # 입력 검증
            is_valid, error_message = self.security.validate_question(question)
            if not is_valid:
                raise ValueError(error_message)
            
            # 안전한 프롬프트 생성
            prompt = self.security.create_safe_prompt(question, context)
            
            # API 호출
            messages = [
                {"role": "system", "content": "당신은 PDF 문서의 내용에 대해 답변하는 도우미입니다."},
                {"role": "user", "content": prompt}
            ]
            
            response = self.create_chat_completion(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response
        except Exception as e:
            raise ValueError(f"PDF Q&A 생성 실패: {str(e)}")
    
    def estimate_tokens(self, text: str) -> int:
        """대략적인 토큰 수를 추정합니다."""
        # 간단한 토큰 추정 (실제로는 tiktoken 라이브러리 사용 권장)
        return len(text) // 4 