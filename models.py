from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id= Column(Integer, primary_key=True, index=True)
    name= Column(String(250))
    email= Column(String(250))
    username= Column(String(250))
    password= Column(String(250))
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class Contact(Base):
    __tablename__='contacts'
    id= Column(Integer, primary_key=True, index=True)
    name= Column(String(250))
    title= Column(String(250))
    email= Column(String(250))
    content= Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

