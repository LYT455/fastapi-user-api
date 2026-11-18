from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # 增加 email 字段，作为登录账号
    email = Column(String(50), unique=True, index=True)
    name = Column(String(50), index=True)
    # 增加 password 字段，用来存加密后的密码
    password = Column(String(100))