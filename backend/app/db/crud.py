from sqlalchemy.orm import Session
from app.models.schemas import UserCreate
from app.core.security import hash_password
from app.db import database

# User table model (inline for simplicity)
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(database.Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True)
    username   = Column(String, unique=True)
    hashed_pw  = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_pw=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user