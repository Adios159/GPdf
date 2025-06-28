from openai import OpenAI
from app.config import settings


class GPTSummarizer:
    """GPT-3.5를 활용한 텍스트 요약 클래스"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def summarize_text(self, text: str, max_tokens: int = 500) -> str:
        """텍스트를 요약합니다."""
        try:
            # 텍스트가 너무 길면 자르기
            if len(text) > 8000:  # GPT-3.5의 토큰 제한 고려
                text = text[:8000]
            
            prompt = f"""
다음 PDF 문서의 내용을 한국어로 요약해주세요. 
주요 내용과 핵심 포인트를 간결하고 명확하게 정리해주세요.

문서 내용:
{text}

요약:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 문서 요약 전문가입니다. 주어진 텍스트의 핵심 내용을 간결하고 명확하게 요약해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise ValueError(f"요약 생성 실패: {str(e)}")
    
    def estimate_cost(self, text: str) -> float:
        """대략적인 API 비용을 추정합니다."""
        # GPT-3.5-turbo의 대략적인 토큰 비용 계산
        estimated_tokens = len(text) // 4  # 대략적인 토큰 계산
        input_cost = (estimated_tokens / 1000) * 0.0015  # $0.0015 per 1K tokens
        output_cost = (500 / 1000) * 0.002  # $0.002 per 1K tokens (최대 출력)
        return input_cost + output_cost 