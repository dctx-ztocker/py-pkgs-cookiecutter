from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["ui"])

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def ui_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("ui.html", {"request": request})
