from pydantic import BaseModel, Field
from typing import Literal


class ConvertRequest(BaseModel):
    """문서 변환 요청 모델"""
    summary_text: str = Field(..., description="요약된 텍스트")
    format: Literal["docx", "pdf", "txt"] = Field(..., description="변환할 파일 형식")
    session_id: str = Field(..., description="세션 ID")


class UsageRequest(BaseModel):
    """사용량 확인 요청 모델"""
    session_id: str = Field(..., description="세션 ID")


class PDFQARequest(BaseModel):
    """PDF Q&A 요청 모델"""
    question: str = Field(..., description="PDF 내용에 대한 질문")
    file_id: str = Field(..., description="질문할 PDF 파일의 ID") 