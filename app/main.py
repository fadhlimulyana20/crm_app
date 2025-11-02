from dotenv import find_dotenv, load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    loaded = load_dotenv(find_dotenv())
    if not loaded:
        # fallback: warn once — replace with logger if needed
        print("Warning: .env file not found; environment variables may be missing")

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers.hello import router as hello_router
from app.controllers.customer import router as customer_router, html_router as customer_html_router
from app.controllers.auth import router as auth_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static/dist"), name="static")

# HTML routes
app.include_router(hello_router)
app.include_router(auth_router, prefix="/auth")
app.include_router(customer_html_router)

# API routes
app.include_router(customer_router, prefix="/api")