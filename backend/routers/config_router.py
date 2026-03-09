from fastapi import APIRouter

from ..config import read_country_list, read_news_topics
from ..models import ConfigResponse

router = APIRouter()


@router.get("/countries", response_model=ConfigResponse)
async def get_countries():
    return ConfigResponse(items=read_country_list())


@router.get("/topics", response_model=ConfigResponse)
async def get_topics():
    return ConfigResponse(items=read_news_topics())
