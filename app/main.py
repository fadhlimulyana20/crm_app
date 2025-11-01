from fastapi import FastAPI
from app.controllers.hello import router as hello_router

app = FastAPI()

app.include_router(hello_router)