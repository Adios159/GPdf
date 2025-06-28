import os
import hashlib
from datetime import datetime
from typing import Optional


def generate_filename(original_filename: str, prefix: str = "", suffix: str = "") -> str:
    """고유한 파일명을 생성합니다."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_filename)
    return f"{prefix}{name}_{timestamp}{suffix}{ext}"


def get_file_hash(file_content: bytes) -> str:
    """파일 내용의 해시값을 계산합니다."""
    return hashlib.md5(file_content).hexdigest()


def validate_file_size(file_content: bytes, max_size: int) -> bool:
    """파일 크기가 제한 내에 있는지 확인합니다."""
    return len(file_content) <= max_size


def get_file_extension(filename: str) -> str:
    """파일 확장자를 반환합니다."""
    return os.path.splitext(filename)[1].lower()


def is_pdf_file(filename: str) -> bool:
    """PDF 파일인지 확인합니다."""
    return get_file_extension(filename) == '.pdf'


def cleanup_old_files(directory: str, max_age_hours: int = 24) -> int:
    """오래된 파일들을 정리합니다."""
    if not os.path.exists(directory):
        return 0
    
    current_time = datetime.now()
    deleted_count = 0
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            age_hours = (current_time - file_time).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception:
                    pass  # 파일 삭제 실패 시 무시
    
    return deleted_count 