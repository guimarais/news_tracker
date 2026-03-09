# News Tracker

A news scraper that monitors media outlets across multiple countries on configurable topics. Each article is summarized into one paragraph and classified as **biased** or **unbiased** using Claude AI.

## Features

- Fetches live news from Google News RSS for any combination of country and topic
- AI-powered one-paragraph summaries via Claude (`claude-sonnet-4-6`)
- Bias classification with reasoning for each article
- Results cached in memory — repeated requests are instant
- Filter articles by country, topic, or bias classification
- On-demand cache refresh from the UI

## Requirements

- Python 3.13+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+ with npm
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:guimarais/news_tracker.git
cd news_tracker
```

### 2. Configure your API key

```bash
cp .env.example .env
# Edit .env and set your key:
# ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Configure countries and topics

Edit `.country_list` (one ISO 3166-1 alpha-2 country code per line):

```
US
GB
DE
PT
```

Edit `.news_topics` (one topic per line):

```
nuclear energy
artificial intelligence
climate change
```

Lines starting with `#` are treated as comments and ignored.

### 4. Install dependencies

```bash
# Backend
uv sync

# Frontend
cd frontend && npm install
```

## Running

Start the backend and frontend in separate terminals:

```bash
# Terminal 1 — backend (http://localhost:8000)
uv run news-check

# Terminal 2 — frontend (http://localhost:4200)
cd frontend && npm start
```

Then open [http://localhost:4200](http://localhost:4200) in your browser.

## Usage

1. Select a **country** and **topic** from the dropdowns — articles load automatically.
2. Use the **bias filter** to show only biased or unbiased articles.
3. Click any article title to open the original source.
4. Expand **Bias reasoning** on a card to read Claude's explanation.
5. Click **Refresh all** to clear the cache and re-fetch everything in the background.

> **Note:** The first request for each country/topic combination calls the Anthropic API for every article, so it may take a few seconds. Subsequent requests for the same pair are served from the in-memory cache instantly.

## API Reference

The backend exposes a REST API documented interactively at [http://localhost:8000/docs](http://localhost:8000/docs).

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/news?country=US&topic=ai` | Fetch (and analyze) articles for a country/topic |
| `GET` | `/api/news/status` | Cache stats and refresh status |
| `POST` | `/api/news/refresh` | Clear cache and re-fetch all combinations |
| `GET` | `/api/config/countries` | List of countries from `.country_list` |
| `GET` | `/api/config/topics` | List of topics from `.news_topics` |

## Project Structure

```
news_tracker/
├── .country_list          # Country codes to monitor
├── .news_topics           # Topics to search for
├── .env                   # API keys (not committed)
├── main.py                # Entry point — starts uvicorn
├── pyproject.toml         # Python dependencies (managed by uv)
│
├── backend/
│   ├── app.py             # FastAPI app, CORS configuration
│   ├── config.py          # Settings, reads config files
│   ├── models.py          # Pydantic data models
│   ├── store.py           # In-memory article cache
│   ├── services/
│   │   ├── news_fetcher.py  # Google News RSS fetching
│   │   └── analyzer.py      # Claude API integration
│   └── routers/
│       ├── news.py          # /api/news endpoints
│       └── config_router.py # /api/config endpoints
│
└── frontend/              # Angular 17 application
    └── src/app/
        ├── app.component.*         # Root component, filter state
        ├── models/article.model.ts
        ├── services/news.service.ts
        └── components/
            ├── news-list/  # Article grid
            └── news-card/  # Individual article card
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Required for summaries and bias analysis |
| `MAX_ARTICLES_PER_QUERY` | `5` | Max articles fetched per country/topic pair |

If `ANTHROPIC_API_KEY` is not set, articles are still fetched but will not be summarized or classified.

## Supported Countries

Any ISO 3166-1 alpha-2 country code can be added to `.country_list`. The following have optimized language settings for Google News:

`US` `GB` `DE` `FR` `ES` `IT` `JP` `BR` `IN` `AU` `CA` `MX` `PT` `AR` `ZA` `NG` `CN` `RU` `KR` `NL` `SE` `PL`

Countries not in this list default to English-language results.
