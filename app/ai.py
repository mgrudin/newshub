import anthropic
from dotenv import load_dotenv

from app.db import SessionLocal
from app.models import Article

load_dotenv()

client = anthropic.Anthropic()

SUMMARY_PROMPT = "Resume the article in 2-3 sentences."


def summarize_article(article_text: str) -> str:
    message = client.messages.create(
        model = "claude-haiku-4-5-20251001",
        max_tokens = 50,
        system = SUMMARY_PROMPT,
        messages = [{"role": "user", "content": article_text}],
    )
    return message.content[0].text


def summarize_and_save(article_id: int) -> str | None:
  with SessionLocal() as session:
    article = session.get(Article, article_id)
    if article:
      if not article.raw:
        print(f"Article {article_id} has no raw content")
        return
      try:
        summary = summarize_article(article.raw)
        article.summary = summary
        session.commit()
        return summary
      except Exception as e:
        print(f"Failed to summarize article {article_id}: {e}")
