from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from app.models.customer import Customer as CustomerModel, create_customer, get_customer, get_customers, update_customer, delete_customer
from app.schema.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schema.generic import GenericResponse, MetaSchema

router = APIRouter(prefix="/customers", tags=["customers"]) # API Router
html_router = APIRouter(prefix="/customers", tags=["customers"]) # HTML Routers

@router.post("/", response_model=GenericResponse[CustomerResponse])
def create_customer_endpoint(customer: CustomerCreate):
    try:
        db_customer = create_customer(**customer.dict())
        return GenericResponse[CustomerResponse](data=CustomerResponse.model_validate(db_customer))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{customer_id}", response_model=GenericResponse[CustomerResponse])
def read_customer(customer_id: int):
    db_customer = get_customer(customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    response = GenericResponse[CustomerResponse](data=CustomerResponse.model_validate(db_customer))
    return response

@router.get("/")
def read_customers(search: Optional[str] = None, skip: int = 0, limit: int = 10):
    customers, total_count = get_customers(search=search, skip=skip, limit=limit)
    page = (skip // limit) + 1
    total_page = (total_count + limit - 1) // limit

    meta = MetaSchema(page=page, total_page=total_page, limit=limit)

    return GenericResponse[List[CustomerResponse]](
        data=[CustomerResponse.model_validate(c) for c in customers], 
        meta=meta
    )

@router.put("/{customer_id}", response_model=GenericResponse[CustomerResponse])
def update_customer_endpoint(customer_id: int, customer: CustomerUpdate):
    db_customer = update_customer(customer_id, **customer.dict(exclude_unset=True))
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return GenericResponse[CustomerResponse](data=CustomerResponse.model_validate(db_customer))

@router.delete("/{customer_id}")
def delete_customer_endpoint(customer_id: int):
    success = delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}

# HTML Route for displaying customer data (template only, data via Alpine.js)
templates = Jinja2Templates(directory="app/templates")

@html_router.get("/", response_class=HTMLResponse)
async def customers_page(request: Request):
    return templates.TemplateResponse("customers.html", {"request": request})