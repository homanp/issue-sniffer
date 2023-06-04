from fastapi import APIRouter

from app.api import ingest, issues

router = APIRouter()
api_prefix = "/api/v1"

router.include_router(ingest.router, tags=["Ingest"], prefix=api_prefix)
router.include_router(issues.router, tags=["Issues"], prefix=api_prefix)
