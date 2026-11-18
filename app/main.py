from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import engine, get_db
from pydantic import BaseModel
import requests

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ============ 直接写在 main.py 里的 AI 接口 ============
class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat", tags=["AI 对话"])
def chat_with_ai(request: ChatRequest):
    # 换你新生成的 Key
    API_KEY = "sk-你的Key填这里"
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": request.prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return {"answer": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
# ====================================================

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)