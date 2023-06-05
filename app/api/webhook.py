from fastapi import APIRouter, Request, HTTPException, status
from app.lib.ingest import ingest
from app.lib.issues import predict

router = APIRouter()


@router.post(
    "/webhook", name="Webhook", description="Github issues code sniffer webhook"
)
async def issues(request: Request):
    """Webhook used by Github"""
    body = await request.json()
    action = body["action"]

    if action == "created":
        await ingest(body)

    elif action == "opened":
        await predict(body)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request",
        )

    return {"success": True}
