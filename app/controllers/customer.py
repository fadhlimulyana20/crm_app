from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.models.customer import Customer as CustomerModel, create_customer, get_customer, get_customers, update_customer, delete_customer

router = APIRouter(prefix="/customers", tags=["customers"])

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    company: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

@router.post("/", response_model=CustomerResponse)
def create_customer_endpoint(customer: CustomerCreate):
    try:
        db_customer = create_customer(**customer.dict())
        return CustomerResponse.from_orm(db_customer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int):
    db_customer = get_customer(customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse.from_orm(db_customer)

@router.get("/", response_model=List[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100):
    customers = get_customers(skip=skip, limit=limit)
    return [CustomerResponse.from_orm(c) for c in customers]

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(customer_id: int, customer: CustomerUpdate):
    db_customer = update_customer(customer_id, **customer.dict(exclude_unset=True))
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse.from_orm(db_customer)

@router.delete("/{customer_id}")
def delete_customer_endpoint(customer_id: int):
    success = delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}