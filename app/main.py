from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router

app = FastAPI(
    title="Issue sniffer",
    description="Let AI sniff out issues in your code",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
