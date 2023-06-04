import uuid

import pinecone
from decouple import config
from fastapi import APIRouter
from langchain.document_loaders import GitLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from pydantic import BaseModel

pinecone.init(
    api_key=config("PINECONE_API_KEY"),
    environment=config("PINECONE_ENVIRONMENT"),
)


router = APIRouter()


class Ingest(BaseModel):
    name: str
    url: str
    branch: str
    file_ending: str


@router.post("/ingest", name=" Ingest", description="Ingest Github repo")
async def issues(body: Ingest):
    """Ingest a Github repo to Pinecone"""
    repo_id = uuid.uuid4()
    repo_path = f"./repos/{repo_id}/"
    embeddings = OpenAIEmbeddings()

    try:
        loader = GitLoader(
            clone_url=body.url,
            repo_path=repo_path,
            branch=body.branch,
            file_filter=lambda file_path: file_path.endswith(body.file_ending),
        )

    except Exception:
        loader = GitLoader(
            repo_path=repo_path,
            branch=body.branch,
            file_filter=lambda file_path: file_path.endswith(body.file_ending),
        )

    docs = loader.load()

    Pinecone.from_documents(
        docs, embeddings, index_name="issue-sniffer", namespace=str(repo_id)
    )

    return {"success": True, "data": str(repo_id)}
