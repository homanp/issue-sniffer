import os

from decouple import config
from fastapi import APIRouter
from github import Github, GithubIntegration
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from pydantic import BaseModel

from app.lib.prompts import PROMPT

router = APIRouter()
app_id = config("GITHUB_APP_ID")

with open(os.path.normpath(os.path.expanduser("./bot_key.pem")), "r") as cert_file:
    app_key = cert_file.read()

git_integration = GithubIntegration(
    app_id,
    app_key,
)


class Issue(BaseModel):
    action: str
    issue: dict
    repository: dict


@router.post("/issues", name=" Issues", description="Github issues code sniffer")
async def issues(body: Issue):
    """Webhook used by Github to POST an issue of type bug"""
    pinecone_namespace = str(body.repository["id"])
    issue_title = body.issue["title"]
    issue_action = body.action
    issue_number = body.issue["number"]
    repo_name = body.repository["name"]
    owner = body.repository["owner"]["login"]
    is_bug = False

    for label in body.issue["labels"]:
        if label["name"] == "bug":
            is_bug = True

    if is_bug and issue_title and issue_action == "opened":
        git_connection = Github(
            login_or_token=git_integration.get_access_token(
                git_integration.get_installation(owner, repo_name).id
            ).token
        )
        repo = git_connection.get_repo(f"{owner}/{repo_name}")
        issue = repo.get_issue(number=issue_number)
        embeddings = OpenAIEmbeddings()
        docsearch = Pinecone.from_existing_index(
            config("PINECONE_INDEX_NAME"),
            embedding=embeddings,
            namespace=pinecone_namespace,
        )
        chain_type_kwargs = {"prompt": PROMPT}
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4", temperature=0, verbose=True),
            chain_type="stuff",
            retriever=docsearch.as_retriever(),
            chain_type_kwargs=chain_type_kwargs,
        )
        output = qa.run(issue_title)
        issue.create_comment(output)

    return {"success": True}
