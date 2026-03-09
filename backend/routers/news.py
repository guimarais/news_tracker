import asyncio

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from ..config import read_country_list, read_news_topics, settings
from ..models import Article, NewsResponse, StatusResponse
from ..services.analyzer import analyze_article
from ..services.news_fetcher import fetch_articles
from .. import store

router = APIRouter()


@router.get("/", response_model=NewsResponse)
async def get_news(
    country: str = Query(..., description="ISO 3166-1 alpha-2 country code"),
    topic: str = Query(..., description="News topic to search for"),
):
    cached = store.get(country, topic)
    if cached is not None:
        return NewsResponse(articles=cached, total=len(cached), country=country, topic=topic)

    articles = await fetch_articles(country, topic, settings.max_articles_per_query)

    if not articles:
        store.set(country, topic, [])
        return NewsResponse(articles=[], total=0, country=country, topic=topic)

    analyzed = await asyncio.gather(*[analyze_article(a) for a in articles])
    result = list(analyzed)
    store.set(country, topic, result)

    return NewsResponse(articles=result, total=len(result), country=country, topic=topic)


@router.get("/status", response_model=StatusResponse)
async def get_status():
    return StatusResponse(**store.get_status())


@router.post("/refresh")
async def refresh_news(background_tasks: BackgroundTasks):
    """Clears the cache and re-fetches all country/topic combinations in the background."""
    store.clear()
    countries = read_country_list()
    topics = read_news_topics()
    background_tasks.add_task(_refresh_all, countries, topics)
    return {"message": "Refresh started", "countries": countries, "topics": topics}


async def _refresh_all(countries: list[str], topics: list[str]) -> None:
    store.set_refreshing(True)
    try:
        tasks = [
            _fetch_and_store(country, topic)
            for country in countries
            for topic in topics
        ]
        await asyncio.gather(*tasks)
    finally:
        store.set_refreshing(False)


async def _fetch_and_store(country: str, topic: str) -> None:
    articles = await fetch_articles(country, topic, settings.max_articles_per_query)
    if articles:
        analyzed = await asyncio.gather(*[analyze_article(a) for a in articles])
        store.set(country, topic, list(analyzed))
    else:
        store.set(country, topic, [])
