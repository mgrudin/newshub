from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from app.articles import fetch_source
from app.db import SessionLocal
from app.models import Source

templates = Jinja2Templates(directory="templates")

app = FastAPI()
sources = []

with SessionLocal() as session:
    sources = session.scalars(select(Source)).all()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"sources": sources}
    )
