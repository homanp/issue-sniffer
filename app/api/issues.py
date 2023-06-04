from fastapi import APIRouter
from pydantic import BaseModel
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from app.lib.prompts import PROMPT

router = APIRouter()


class Issue(BaseModel):
    issue: dict


@router.post("/issues", name=" Issues", description="Github issues code sniffer")
async def issues(body: Issue):
    """Webhook used by Github to POST an issue of type bug"""
    pinecone_namespace = "02a98cd2-0034-43ee-b745-c1294bcff0f2"
    is_bug = False

    for label in body.issue["labels"]:
        if label["name"] == "bug":
            is_bug = True

    if is_bug:
        embeddings = OpenAIEmbeddings()
        docsearch = Pinecone.from_existing_index(
            "issue-sniffer", embedding=embeddings, namespace=pinecone_namespace
        )
        chain_type_kwargs = {"prompt": PROMPT}
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4", temperature=0, verbose=True),
            chain_type="stuff",
            retriever=docsearch.as_retriever(),
            chain_type_kwargs=chain_type_kwargs,
        )
        output = qa.run(body.issue["title"])

        return {"success": True, "data": output}

    return {"success": True}
