# flake8: noqa
from langchain.prompts import PromptTemplate

prompt_template = """You are an AI assistant that helps developers to find bugs in their 
code by analyzing the following pieces of context to find the bug or issue statued in the issue title below. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Issue title: {question}
Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
