from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.types import String
from app.database import Base


class Mutation(Base):
    __tablename__= "mutation"
    id = Column(String, primary_key=True, index=True)
    nomor_rekening= Column(String)
    time = Column(String)
    transaction_code = Column(String)
    nominal = Column(Integer)
