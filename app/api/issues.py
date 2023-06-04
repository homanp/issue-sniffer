from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Issue(BaseModel):
    issue: dict


@router.post("/issues", name=" Issues", description="Github issues code sniffer")
async def issues(body: Issue):
    """Webhook used by Github to POST an issue of type bug"""
    print(body)
    return {"success": True, "data": body}
