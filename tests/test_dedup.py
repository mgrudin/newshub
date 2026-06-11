import feedparser
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.articles
from app.articles import fetch_source
from app.db import Base
from app.models import Article, Source


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    # Test database setup
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    monkeypatch.setattr(app.articles, "SessionLocal", TestSession)
    return TestSession


def test_fetch_source_dedupes(test_db, monkeypatch):
    # Arrange: кладём источник в тестовую БД
    with test_db() as session:
        source = Source(url="http://feed.test/rss")
        session.add(source)
        session.commit()
        source_id = source.id

    # подделка feedparser.parse -> две статьи (FeedParserDict ведёт себя
    # как настоящий entry: поддерживает и .get("link"), и .link)
    fake_feed = feedparser.FeedParserDict(
        entries=[
            feedparser.FeedParserDict(link="http://a/1", title="A1", summary="s1"),
            feedparser.FeedParserDict(link="http://a/2", title="A2", summary="s2"),
        ]
    )
    monkeypatch.setattr(app.articles.feedparser, "parse", lambda url: fake_feed)

    first_result = fetch_source(source_id)
    assert first_result == 2

    second_result = fetch_source(source_id)
    assert second_result == 0
