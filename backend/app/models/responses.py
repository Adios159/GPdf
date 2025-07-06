from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SummarizeResponse(BaseModel):
    """PDF 요약 응답 모델"""
    summary: str = Field(..., description="요약된 텍스트")
    page_count: int = Field(..., description="처리된 페이지 수")
    usage_remaining: int = Field(..., description="남은 사용 횟수")
    processing_time: float = Field(..., description="처리 시간(초)")


class ConvertResponse(BaseModel):
    """문서 변환 응답 모델"""
    download_url: str = Field(..., description="다운로드 URL")
    filename: str = Field(..., description="파일명")
    file_size: int = Field(..., description="파일 크기(바이트)")


class UsageResponse(BaseModel):
    """사용량 응답 모델"""
    usage_count: int = Field(..., description="사용 횟수")
    limit: int = Field(..., description="일일 제한")
    remaining: int = Field(..., description="남은 횟수")
    reset_time: datetime = Field(..., description="리셋 시간")


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="상세 정보")
    error_code: Optional[str] = Field(None, description="에러 코드")


class PDFQAResponse(BaseModel):
    """PDF Q&A 응답 모델"""
    answer: str = Field(..., description="질문에 대한 답변")
    context: str = Field(..., description="답변의 근거가 된 PDF 내용") 