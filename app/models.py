from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # 注意这里：把 String 改成 String(50)
    name = Column(String(50), index=True)