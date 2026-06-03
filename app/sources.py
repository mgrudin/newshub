import feedparser
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models import Source


def add_source(url: str) -> Source:
    feed = feedparser.parse(url)

    if not feed.version:
        raise ValueError(f"Not a valid feed: {url}")

    with SessionLocal() as session:
        source = Source(url=url, title=feed.feed.get("title"))
        session.add(source)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError(f"Source already exists: {url}")
        session.refresh(source)
        return source
