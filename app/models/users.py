
from sqlalchemy import Column, String, Integer
from sqlalchemy.types import String
from app.database import Base


class Users(Base):
    __tablename__= "users"
    id = Column(String, primary_key=True, index=True)
    nomor_rekening = Column(String)
    phone_number = Column(String)
    nik = Column(String)
    pin = Column(String)
    saldo = Column(Integer)
