from fastapi import APIRouter

from app.api import webhook

router = APIRouter()
api_prefix = "/api/v1"

router.include_router(webhook.router, tags=["Webhook"], prefix=api_prefix)
