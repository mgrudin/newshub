"""Done-test of pipeline RSS: add_source -> fetch_source (+ dedup)."""

from sqlalchemy import delete, select

from app.articles import fetch_source
from app.db import SessionLocal
from app.models import Article, Source
from app.sources import add_source

TEST_FEED = "https://hnrss.org/frontpage"


def cleanup():
    """Delete old test data to make the test reproducible."""
    with SessionLocal() as session:
        src = session.scalar(select(Source).where(Source.url == TEST_FEED))
        if src:
            session.execute(delete(Article).where(Article.source_id == src.id))
            session.delete(src)
            session.commit()


def main():
    cleanup()

    # 1) add_source: source should save and get id
    source = add_source(TEST_FEED)
    assert source.id is not None, "Source does not save"
    print(f"[ok] source is created: id={source.id}, title={source.title!r}")

    # 2) first fetch: should appear articles
    first = fetch_source(source.id)
    print(f"[ok] first fetch: {first} new articles")
    assert first > 0, "Expected new articles on the first fetch"

    # 3) second fetch: dedup -> 0 new, no IntegrityError
    second = fetch_source(source.id)
    status = "ok" if second == 0 else "FAIL"
    print(f"[{status}] second fetch: {second} new articles (expected 0)")
    assert second == 0, "Dedup does not work: articles appeared on the second pass"

    # 4) check how one article was filled
    with SessionLocal() as session:
        art = session.scalar(select(Article).where(Article.source_id == source.id))
        print("\narticle example:")
        print("  title    :", art.title)
        print("  link     :", art.link)
        print("  published:", art.published)
        print("  raw      :", (art.raw or "")[:60], "...")
        print("  summary  :", art.summary, "(expected None before Phase 2)")
        assert art.link, "link is empty"
        assert art.summary is None, "summary should be None before Phase 2"

    print("\nDONE-Test passed")


if __name__ == "__main__":
    main()
