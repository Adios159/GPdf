from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import FileResponse
import time
import os
from datetime import datetime

from app.models.requests import ConvertRequest, PDFQARequest
from app.models.responses import SummarizeResponse, ConvertResponse, UsageResponse, ErrorResponse, PDFQAResponse
from app.core.pdf_processor import PDFProcessor
from app.core.summarizer import GPTSummarizer
from app.core.converter import DocumentConverter
from app.core.rate_limiter import RateLimiter
from app.config import settings
from app.utils.openai_client import OpenAIClient

router = APIRouter()

# Initialize services
pdf_processor = PDFProcessor()
summarizer = GPTSummarizer()
rate_limiter = RateLimiter()
openai_client = OpenAIClient()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_pdf(
    file: UploadFile = File(...),
    session_id: str = Form(...)
):
    """PDF 파일을 업로드하고 요약을 생성합니다."""
    
    start_time = time.time()
    
    try:
        # 1. 사용량 제한 확인
        usage_info = rate_limiter.check_limit(session_id)
        if usage_info["remaining"] <= 0:
            raise HTTPException(
                status_code=429,
                detail="일일 사용 한도를 초과했습니다. 내일 다시 시도해주세요."
            )
        
        # 2. 파일 검증
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="PDF 파일만 업로드 가능합니다."
            )
        
        # 3. 파일 크기 확인
        contents = await file.read()
        if len(contents) > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"파일 크기가 {settings.max_file_size // (1024*1024)}MB를 초과합니다."
            )
        
        # 4. PDF 유효성 검증
        if not pdf_processor.validate_pdf(contents):
            raise HTTPException(
                status_code=400,
                detail="유효하지 않은 PDF 파일입니다."
            )
        
        # 5. PDF에서 텍스트 추출
        extracted_text = pdf_processor.extract_text_from_pages(contents, settings.max_pages)
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="PDF에서 텍스트를 추출할 수 없습니다. 이미지 기반 PDF이거나 보호된 파일일 수 있습니다."
            )
        
        # 6. GPT-3.5로 요약 생성
        summary = summarizer.summarize_text(extracted_text)
        
        # 7. 사용량 증가
        rate_limiter.increment_usage(session_id)
        updated_usage = rate_limiter.check_limit(session_id)
        
        processing_time = time.time() - start_time
        
        return SummarizeResponse(
            summary=summary,
            page_count=min(pdf_processor.get_page_count(contents), settings.max_pages),
            usage_remaining=updated_usage["remaining"],
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"처리 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/convert", response_model=ConvertResponse)
async def convert_document(
    summary_text: str = Form(...),
    format: str = Form(...),
    session_id: str = Form(...)
):
    """요약 텍스트를 지정된 형식으로 변환합니다."""
    
    try:
        # 1. 사용량 확인 (요약을 먼저 했는지 확인)
        usage_info = rate_limiter.check_limit(session_id)
        if usage_info["usage_count"] == 0:
            raise HTTPException(
                status_code=400,
                detail="먼저 PDF를 요약해주세요."
            )
        
        # 2. 요약 텍스트 검증
        if not summary_text or len(summary_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="유효한 요약 텍스트가 필요합니다."
            )
        
        # 3. 형식 검증
        if format not in ["docx", "pdf", "txt"]:
            raise HTTPException(
                status_code=400,
                detail="지원하는 형식: docx, pdf, txt"
            )
        
        # 4. 문서 변환
        converter = DocumentConverter()
        
        if format == "docx":
            file_content = converter.to_docx(summary_text)
            filename = f"summary_{int(time.time())}.docx"
        elif format == "pdf":
            file_content = converter.to_pdf(summary_text)
            filename = f"summary_{int(time.time())}.pdf"
        elif format == "txt":
            file_content = converter.to_txt(summary_text)
            filename = f"summary_{int(time.time())}.txt"
        
        # 5. 파일 저장
        file_path = os.path.join("downloads", filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return ConvertResponse(
            download_url=f"/pdf/download/{filename}",
            filename=filename,
            file_size=len(file_content)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"변환 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/usage/{session_id}", response_model=UsageResponse)
async def get_usage(session_id: str):
    """사용량 정보를 조회합니다."""
    
    try:
        usage_info = rate_limiter.check_limit(session_id)
        
        return UsageResponse(
            usage_count=usage_info["usage_count"],
            limit=usage_info["limit"],
            remaining=usage_info["remaining"],
            reset_time=usage_info["reset_time"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"사용량 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/download/{filename}")
async def download_file(filename: str):
    """변환된 파일을 다운로드합니다."""
    
    file_path = os.path.join("downloads", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="파일을 찾을 수 없습니다."
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@router.post("/qa", response_model=PDFQAResponse)
async def ask_question(request: PDFQARequest):
    """PDF 내용을 바탕으로 질문에 답변합니다."""
    try:
        # PDF 파일 내용 가져오기
        pdf_text = pdf_processor.get_pdf_text(request.file_id)
        if not pdf_text:
            raise HTTPException(status_code=404, detail="PDF 파일을 찾을 수 없습니다.")
        
        # OpenAI API를 사용하여 질문에 답변
        response = openai_client.create_pdf_qa(
            question=request.question,
            context=pdf_text
        )
        
        # 응답 생성
        answer = response.choices[0].message.content
        return PDFQAResponse(
            answer=answer,
            context=pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 