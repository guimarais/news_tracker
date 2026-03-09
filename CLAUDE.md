# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**News Check** scrapes Google News RSS for topics (`.news_topics`) across countries (`.country_list`), uses Claude (`claude-sonnet-4-6`) to generate a one-paragraph summary and bias classification for each article, and exposes the results through a FastAPI backend + Angular 17 frontend.

## Commands

### Backend
```bash
# Install dependencies
uv sync

# Run dev server (port 8000, auto-reload)
uv run news-check
# or
uv run uvicorn backend.app:app --reload

# API docs
open http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm start          # dev server on http://localhost:4200
npm run build      # production build → frontend/dist/
```

## Architecture

```
.country_list          # ISO-3166 country codes, one per line
.news_topics           # search topics, one per line
.env                   # ANTHROPIC_API_KEY (copy from .env.example)

backend/
├── app.py             # FastAPI app, CORS (localhost:4200), router registration
├── config.py          # pydantic-settings; reads .country_list / .news_topics from root
├── models.py          # Pydantic: Article, NewsResponse, ConfigResponse, StatusResponse
├── store.py           # in-memory cache dict[(country, topic)] → list[Article]
├── services/
│   ├── news_fetcher.py  # async: httpx fetches Google News RSS, feedparser parses it
│   └── analyzer.py      # asyncio.to_thread wrapper around Anthropic SDK call
└── routers/
    ├── news.py          # GET /api/news?country=&topic=, GET /api/news/status, POST /api/news/refresh
    └── config_router.py # GET /api/config/countries, GET /api/config/topics

frontend/src/app/
├── app.component.*      # root: owns filter state, triggers API calls, holds articles[]
├── models/article.model.ts
├── services/news.service.ts   # HttpClient wrapper for all backend calls
└── components/
    ├── news-list/       # receives articles[] + loading/error state; renders the grid
    └── news-card/       # @Input() article; shows title, source, summary, bias badge
```

### Key data flow

1. On startup, `AppComponent.ngOnInit` loads countries and topics from `/api/config/*`.
2. When the user selects a country + topic, `GET /api/news?country=&topic=` is called.
3. The backend checks the in-memory store; on miss it fetches Google News RSS (httpx async), then calls `analyzer.analyze_article` for each article concurrently (`asyncio.gather`).
4. `analyze_article` runs `_call_claude` in a thread (`asyncio.to_thread`) to avoid blocking the event loop with the synchronous Anthropic SDK.
5. Results are cached in `store.py` and returned. Bias filtering is client-side in Angular.
6. `POST /api/news/refresh` clears the cache and re-fetches everything in the background.

### Google News RSS URL pattern
```
https://news.google.com/rss/search?q={topic}&hl={hl}&gl={country_code}&ceid={country_code}:{lang}
```
Country → (hl, ceid_lang) mapping lives in `backend/services/news_fetcher.py:COUNTRY_CONFIG`.

### Claude prompt
Single user message asking for JSON: `{"summary": "...", "bias": "biased"|"unbiased", "bias_reasoning": "..."}`.
Response is extracted with a `re.search(r"\{.*\}", text, re.DOTALL)` to handle markdown code-block wrapping.
