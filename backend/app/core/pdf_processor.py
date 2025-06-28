import fitz  # PyMuPDF
from typing import Union


class PDFProcessor:
    """PDF 파일 처리를 담당하는 클래스"""
    
    def extract_text_from_pages(self, file_content: bytes, max_pages: int = 3) -> str:
        """PDF에서 지정된 페이지까지의 텍스트를 추출합니다."""
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            
            # 최대 페이지 수만큼 텍스트 추출
            for page_num in range(min(len(doc), max_pages)):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            return text.strip()
            
        except Exception as e:
            raise ValueError(f"PDF 텍스트 추출 실패: {str(e)}")
    
    def validate_pdf(self, file_content: bytes) -> bool:
        """PDF 파일이 유효한지 검증합니다."""
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            is_valid = len(doc) > 0
            doc.close()
            return is_valid
        except:
            return False
    
    def get_page_count(self, file_content: bytes) -> int:
        """PDF의 총 페이지 수를 반환합니다."""
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            page_count = len(doc)
            doc.close()
            return page_count
        except:
            return 0 