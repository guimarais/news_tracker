from pydantic import BaseModel
from typing import Literal


class Article(BaseModel):
    id: str
    title: str
    url: str
    source: str = ""
    country: str
    topic: str
    published_at: str = ""
    description: str = ""
    summary: str | None = None
    bias: Literal["biased", "unbiased"] | None = None
    bias_reasoning: str | None = None
    analyzed: bool = False


class NewsResponse(BaseModel):
    articles: list[Article]
    total: int
    country: str
    topic: str


class ConfigResponse(BaseModel):
    items: list[str]


class StatusResponse(BaseModel):
    total_articles: int
    analyzed_articles: int
    is_refreshing: bool
