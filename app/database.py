import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 判断是否在Docker容器内运行（容器内会存在 /.dockerenv 文件）
if os.path.exists('/.dockerenv'):
    # 容器环境：使用 host.docker.internal
    DB_HOST = "host.docker.internal"
else:
    # 本地环境：使用 127.0.0.1
    DB_HOST = "127.0.0.1"

# 支持通过环境变量覆盖，方便部署到服务器
DB_HOST = os.getenv("DB_HOST", DB_HOST)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:5608lj+-@{DB_HOST}:3306/fastapi_demo"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()