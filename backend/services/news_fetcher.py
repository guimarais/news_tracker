import asyncio
import hashlib
import re
from urllib.parse import quote

import feedparser
import httpx

from ..models import Article

# Maps country code -> (hl, ceid_lang)
# Using English for all countries so Claude can analyze consistently.
# The gl parameter still restricts results to that country's Google News section.
COUNTRY_CONFIG: dict[str, tuple[str, str]] = {
    "US": ("en-US", "en"),
    "GB": ("en-GB", "en"),
    "DE": ("de", "de"),
    "FR": ("fr", "fr"),
    "ES": ("es", "es"),
    "IT": ("it", "it"),
    "JP": ("ja", "ja"),
    "BR": ("pt-BR", "pt-BR"),
    "IN": ("en-IN", "en"),
    "AU": ("en-AU", "en"),
    "CA": ("en-CA", "en"),
    "MX": ("es-419", "es-419"),
    "PT": ("pt-PT", "pt-PT"),
    "AR": ("es-419", "es-419"),
    "ZA": ("en-ZA", "en"),
    "NG": ("en", "en"),
    "CN": ("zh-CN", "zh-CN"),
    "RU": ("ru", "ru"),
    "KR": ("ko", "ko"),
    "NL": ("nl", "nl"),
    "SE": ("sv", "sv"),
    "PL": ("pl", "pl"),
}


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text).strip()


def _parse_feed(content: str, country: str, topic: str, max_results: int) -> list[Article]:
    feed = feedparser.parse(content)
    articles: list[Article] = []

    for entry in feed.entries[:max_results]:
        title = entry.get("title", "").strip()
        if not title:
            continue

        source_name = ""
        source = entry.get("source", {})
        if isinstance(source, dict):
            source_name = source.get("title", "")

        # Google News embeds source in title: "Article Title - Source Name"
        if not source_name and " - " in title:
            parts = title.rsplit(" - ", 1)
            if len(parts) == 2:
                title, source_name = parts[0].strip(), parts[1].strip()

        url = entry.get("link", "")
        article_id = hashlib.md5(url.encode()).hexdigest()
        description = _strip_html(entry.get("summary", ""))

        articles.append(
            Article(
                id=article_id,
                title=title,
                url=url,
                source=source_name,
                country=country,
                topic=topic,
                published_at=entry.get("published", ""),
                description=description,
            )
        )

    return articles


async def fetch_articles(country: str, topic: str, max_results: int = 5) -> list[Article]:
    code = country.upper()
    hl, ceid_lang = COUNTRY_CONFIG.get(code, ("en", "en"))
    encoded_topic = quote(topic)
    url = (
        f"https://news.google.com/rss/search"
        f"?q={encoded_topic}&hl={hl}&gl={code}&ceid={code}:{ceid_lang}"
    )

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            response = await client.get(url)
            content = response.text
    except Exception:
        return []

    # feedparser is CPU-bound / sync — run in thread to avoid blocking event loop
    return await asyncio.to_thread(_parse_feed, content, country, topic, max_results)
