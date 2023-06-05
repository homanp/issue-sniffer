import pinecone
from decouple import config
from fastapi import APIRouter
from langchain.document_loaders import GitLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from pydantic import BaseModel

from app.lib.constants import FILE_PATH_WHITELIST

pinecone.init(
    api_key=config("PINECONE_API_KEY"),
    environment=config("PINECONE_ENVIRONMENT"),
)


router = APIRouter()


class Ingest(BaseModel):
    repositories: list


@router.post("/ingest", name=" Ingest", description="Ingest Github repo")
async def issues(body: Ingest):
    """Ingest a Github repo to Pinecone"""
    for repository in body.repositories:
        repo_id = repository["id"]
        repo_name = repository["full_name"]
        repo_url = f"https://github.com/{repo_name}"
        repo_path = f"./repos/{repo_id}/"
        embeddings = OpenAIEmbeddings()

        try:
            loader = GitLoader(
                clone_url=repo_url,
                repo_path=repo_path,
                branch="main",
                file_filter=lambda file_path: any(
                    file_path.endswith(extension) for extension in FILE_PATH_WHITELIST
                ),
            )

        except Exception:
            loader = GitLoader(
                repo_path=repo_path,
                branch="main",
                file_filter=lambda file_path: any(
                    file_path.endswith(extension) for extension in FILE_PATH_WHITELIST
                ),
            )

        docs = loader.load()

        Pinecone.from_documents(
            docs, embeddings, index_name="issue-sniffer", namespace=str(repo_id)
        )

    return {"success": True}
