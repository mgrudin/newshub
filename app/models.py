from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str | None]
    added_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    articles: Mapped[list["Article"]] = relationship(back_populates="source")


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    title: Mapped[str | None]
    link: Mapped[str] = mapped_column(String, unique=True)
    published: Mapped[datetime | None]
    raw: Mapped[str | None]
    summary: Mapped[str | None]
    fetched_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    source: Mapped["Source"] = relationship(back_populates="articles")
