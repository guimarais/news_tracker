from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import news, config_router

app = FastAPI(title="News Check API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(config_router.router, prefix="/api/config", tags=["config"])
