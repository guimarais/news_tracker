from .models import Article

# Keyed by (country, topic)
_cache: dict[tuple[str, str], list[Article]] = {}
_is_refreshing: bool = False


def get(country: str, topic: str) -> list[Article] | None:
    return _cache.get((country.upper(), topic.lower()))


def set(country: str, topic: str, articles: list[Article]) -> None:
    _cache[(country.upper(), topic.lower())] = articles


def get_all() -> list[Article]:
    result = []
    for articles in _cache.values():
        result.extend(articles)
    return result


def clear() -> None:
    _cache.clear()


def get_status() -> dict:
    all_articles = get_all()
    return {
        "total_articles": len(all_articles),
        "analyzed_articles": sum(1 for a in all_articles if a.analyzed),
        "is_refreshing": _is_refreshing,
    }


def set_refreshing(value: bool) -> None:
    global _is_refreshing
    _is_refreshing = value
