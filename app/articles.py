from datetime import UTC, datetime

import feedparser
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Article, Source


def fetch_source(source_id: int) -> int:
    new_articles = 0

    with SessionLocal() as session:
        source = session.get(Source, source_id)

        if not source:
            return new_articles

        feed = feedparser.parse(source.url)

        for entry in feed.entries:
            link = entry.get("link")
            if not link:
                continue

            existing = session.scalar(select(Article).where(Article.link == link))

            if existing:
                continue

            a = add_article(source, entry)
            new_articles += 1
            session.add(a)

        session.commit()
        return new_articles


def add_article(source, entry) -> Article:
    pp = entry.get("published_parsed")
    published = datetime(*pp[:6], tzinfo=UTC) if pp else None
    summary = entry.get("summary")

    article = Article(
        title=entry.get("title"),
        link=entry.get("link"),
        published=published,
        raw=summary,
        source=source,
    )
    return article
