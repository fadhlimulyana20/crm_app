from fastapi import FastAPI
from app.controllers.hello import router as hello_router
from app.controllers.customer import router as customer_router
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(hello_router)
app.include_router(customer_router)