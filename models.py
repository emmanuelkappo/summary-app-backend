from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)


class Quota(Base):
    __tablename__ = "quota"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    quota = Column(Integer, default=10)
    used = Column(Integer, default=0)
