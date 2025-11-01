from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base, SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# CRUD Methods
def create_user(name: str, email: str, username: str, password: str):
    db = SessionLocal()
    try:
        hashed_password = pwd_context.hash(password)
        user = User(name=name, email=email, username=username, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def get_user(user_id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

def get_users(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return db.query(User).offset(skip).limit(limit).all()
    finally:
        db.close()

def update_user(user_id: int, name: str = None, email: str = None, username: str = None, password: str = None):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            if username:
                user.username = username
            if password:
                user.password = pwd_context.hash(password)
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()

def delete_user(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    finally:
        db.close()

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user