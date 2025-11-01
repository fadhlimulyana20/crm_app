from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from app.models.user import User, create_user, authenticate_user, get_users
from app.database import SessionLocal

router = APIRouter()

SECRET = "your-secret-key"  # In production, use environment variable
manager = LoginManager(SECRET, token_url="/auth/login", use_cookie=True)
manager.cookie_name = "auth_cookie"

templates = Jinja2Templates(directory="app/templates")

@manager.user_loader()
def load_user(username: str):
    return get_user_by_username(username)

def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = manager.create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/auth/admin", status_code=302)
    manager.set_cookie(response, access_token)
    return response

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(name: str = Form(...), email: str = Form(...), username: str = Form(...), password: str = Form(...)):
    user = create_user(name, email, username, password)
    return RedirectResponse(url="/auth/login", status_code=302)

@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, user=Depends(manager)):
    users = get_users()
    return templates.TemplateResponse("admin.html", {"request": request, "users": users, "current_user": user})

@router.post("/logout")
def logout():
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie(manager.cookie_name)
    return response