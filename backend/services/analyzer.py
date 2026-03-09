import asyncio
import json
import re

import anthropic

from ..config import settings
from ..models import Article

_PROMPT_TEMPLATE = """\
Analyze the following news article snippet and respond ONLY with valid JSON.

Title: {title}
{description_block}
Provide:
1. A one-paragraph summary of the news story.
2. Whether the article appears "biased" or "unbiased", with a brief reasoning.

Respond strictly in this JSON format (no markdown, no extra text):
{{"summary": "...", "bias": "biased" or "unbiased", "bias_reasoning": "..."}}
"""


def _call_claude(title: str, description: str) -> dict:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    description_block = f"Description: {description}" if description else ""
    prompt = _PROMPT_TEMPLATE.format(title=title, description_block=description_block)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    # Extract JSON even if Claude wraps it in a code block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {}


async def analyze_article(article: Article) -> Article:
    if not settings.anthropic_api_key:
        return article

    content = article.title + article.description
    if len(content.strip()) < 20:
        return article

    try:
        result = await asyncio.to_thread(_call_claude, article.title, article.description)
        article = article.model_copy(
            update={
                "summary": result.get("summary"),
                "bias": result.get("bias"),
                "bias_reasoning": result.get("bias_reasoning"),
                "analyzed": True,
            }
        )
    except Exception:
        pass

    return article
