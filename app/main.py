from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers.hello import router as hello_router
from app.controllers.customer import router as customer_router
from app.controllers.auth import router as auth_router
from app.database import engine, Base
from app.models.user import User

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static/dist"), name="static")

app.include_router(hello_router)
app.include_router(customer_router)
app.include_router(auth_router, prefix="/auth")