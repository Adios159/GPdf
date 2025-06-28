from openai import OpenAI
from app.config import settings


class OpenAIClient:
    """OpenAI API 클라이언트 래퍼"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
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
    
    def estimate_tokens(self, text: str) -> int:
        """대략적인 토큰 수를 추정합니다."""
        # 간단한 토큰 추정 (실제로는 tiktoken 라이브러리 사용 권장)
        return len(text) // 4 