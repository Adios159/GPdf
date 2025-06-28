from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """시스템 상태 확인"""
    return {
        "status": "healthy",
        "service": "GPdf API",
        "version": "1.0.0"
    } 