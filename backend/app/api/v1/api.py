from fastapi import APIRouter

from app.api.v1.endpoints import pdf, health

api_router = APIRouter()
 
# Include all endpoint routers
api_router.include_router(pdf.router, prefix="/pdf", tags=["pdf"])
api_router.include_router(health.router, prefix="/health", tags=["health"]) 