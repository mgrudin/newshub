from typing import Annotated
from urllib.parse import quote

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.articles import fetch_source
from app.db import SessionLocal
from app.models import Article, Source
from app.sources import add_source

templates = Jinja2Templates(directory="templates")

app = FastAPI()
sources = []
articles = []


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, error: str | None = None):
    with SessionLocal() as session:
        sources = session.scalars(
            select(Source).options(selectinload(Source.articles))
        ).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"sources": sources, "error": error},
    )


@app.post("/source")
def create_source(url: Annotated[str, Form()]):
    try:
        source = add_source(url)
    except ValueError as e:
        return RedirectResponse(url=f"/?error={quote(str(e))}", status_code=303)
    fetch_source(source.id)
    return RedirectResponse(url="/", status_code=303)
