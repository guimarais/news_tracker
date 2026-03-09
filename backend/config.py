from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ROOT_DIR / ".env"), env_file_encoding="utf-8")

    anthropic_api_key: str = ""
    max_articles_per_query: int = 5


settings = Settings()


def read_country_list() -> list[str]:
    path = ROOT_DIR / ".country_list"
    if not path.exists():
        return ["US", "GB", "DE", "FR"]
    return [
        line.strip().upper()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]


def read_news_topics() -> list[str]:
    path = ROOT_DIR / ".news_topics"
    if not path.exists():
        return ["technology", "politics", "economy"]
    return [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
