from datetime import datetime, timedelta
from typing import Dict
from app.config import settings


class RateLimiter:
    """사용량 제한을 관리하는 클래스"""
    
    def __init__(self):
        # 메모리 기반 사용량 저장
        self._usage_store: Dict[str, Dict] = {}
    
    def check_limit(self, session_id: str) -> Dict:
        """세션의 사용량 제한을 확인합니다."""
        current_time = datetime.now()
        today = current_time.date()
        
        # 세션 정보가 없으면 새로 생성
        if session_id not in self._usage_store:
            self._usage_store[session_id] = {
                "usage_count": 0,
                "date": today,
                "last_reset": current_time
            }
        
        session_data = self._usage_store[session_id]
        
        # 날짜가 바뀌었으면 사용량 리셋
        if session_data["date"] != today:
            session_data["usage_count"] = 0
            session_data["date"] = today
            session_data["last_reset"] = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        remaining = max(0, settings.daily_limit - session_data["usage_count"])
        
        # 다음 리셋 시간 계산
        next_reset = current_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        return {
            "usage_count": session_data["usage_count"],
            "limit": settings.daily_limit,
            "remaining": remaining,
            "reset_time": next_reset
        }
    
    def increment_usage(self, session_id: str) -> bool:
        """사용량을 증가시킵니다."""
        usage_info = self.check_limit(session_id)
        
        if usage_info["remaining"] <= 0:
            return False
        
        self._usage_store[session_id]["usage_count"] += 1
        return True 