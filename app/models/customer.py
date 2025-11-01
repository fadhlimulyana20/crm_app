from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base, SessionLocal

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    company = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# CRUD Methods
def create_customer(name: str, email: str, phone: str = None, address: str = None, company: str = None):
    db = SessionLocal()
    try:
        customer = Customer(name=name, email=email, phone=phone, address=address, company=company)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    finally:
        db.close()

def get_customer(customer_id: int):
    db = SessionLocal()
    try:
        return db.query(Customer).filter(Customer.id == customer_id).first()
    finally:
        db.close()

def get_customers(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return db.query(Customer).offset(skip).limit(limit).all()
    finally:
        db.close()

def update_customer(customer_id: int, name: str = None, email: str = None, phone: str = None, address: str = None, company: str = None):
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            if name:
                customer.name = name
            if email:
                customer.email = email
            if phone:
                customer.phone = phone
            if address:
                customer.address = address
            if company:
                customer.company = company
            db.commit()
            db.refresh(customer)
        return customer
    finally:
        db.close()

def delete_customer(customer_id: int):
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            db.delete(customer)
            db.commit()
            return True
        return False
    finally:
        db.close()