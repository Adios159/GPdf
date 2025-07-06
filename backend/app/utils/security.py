import re
from typing import Tuple

class SecurityUtils:
    @staticmethod
    def sanitize_input(text: str) -> str:
        """사용자 입력을 정제합니다."""
        # 위험한 문자 및 패턴 제거
        text = re.sub(r'[<>{}]', '', text)
        # 연속된 공백 정리
        text = ' '.join(text.split())
        return text.strip()

    @staticmethod
    def validate_question(question: str) -> Tuple[bool, str]:
        """질문의 유효성을 검사합니다."""
        if not question or len(question.strip()) == 0:
            return False, "질문이 비어있습니다."
        
        if len(question) > 500:
            return False, "질문이 너무 깁니다. (최대 500자)"
        
        # 프롬프트 인젝션 시도 탐지
        suspicious_patterns = [
            r"system:",
            r"assistant:",
            r"user:",
            r"ignore previous",
            r"ignore above",
            r"forget",
            r"new prompt",
            r"\{.*\}",  # JSON 형식
            r"<.*>",    # XML/HTML 태그
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, question, re.IGNORECASE):
                return False, "유효하지 않은 입력입니다."
        
        return True, ""

    @staticmethod
    def create_safe_prompt(question: str, context: str, max_context_length: int = 4000) -> str:
        """안전한 프롬프트를 생성합니다."""
        # 컨텍스트 길이 제한
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
        
        # 프롬프트 템플릿
        template = """
당신은 PDF 문서의 내용에 대해 답변하는 도우미입니다.
아래 제공된 PDF 내용만을 바탕으로 질문에 답변해주세요.
PDF 내용에서 찾을 수 없는 정보에 대해서는 "주어진 PDF 내용에서는 해당 정보를 찾을 수 없습니다."라고 답변해주세요.

PDF 내용:
{context}

질문:
{question}

답변:
"""
        
        # 안전하게 처리된 입력값으로 프롬프트 생성
        safe_question = SecurityUtils.sanitize_input(question)
        safe_context = SecurityUtils.sanitize_input(context)
        
        return template.format(
            context=safe_context,
            question=safe_question
        ) 