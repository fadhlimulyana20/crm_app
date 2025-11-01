from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models.hello import HelloMessage

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def hello_page(request: Request):
    message = HelloMessage()
    return templates.TemplateResponse("hello.html", {"request": request, "message": message.message})

@router.get("/api/hello", response_model=HelloMessage)
async def hello_api():
    return HelloMessage()