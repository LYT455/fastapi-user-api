from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app import crud, schemas, models
from app.database import engine, get_db
from app.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 定义 OAuth2 方案，让 Swagger 知道去哪里登录
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 1. 依赖注入：获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token 无效或已过期，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


# 2. 注册接口
@app.post("/register", response_model=schemas.UserResponse, tags=["认证"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")
    return crud.create_user(db=db, user=user)


# 3. 登录接口
@app.post("/login", tags=["认证"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username 就是我们的邮箱
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="邮箱或密码错误")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# 4. 受保护的接口（必须登录）
@app.get("/users/me", response_model=schemas.UserResponse, tags=["用户管理"])
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# 5. 受保护的 AI 接口
@app.post("/chat", tags=["AI 对话"])
def chat_with_ai(request: schemas.ChatRequest, current_user: models.User = Depends(get_current_user)):
    # ⚠️ 把下面换成你真实的 Key
    API_KEY = "sk-你的key"
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": request.prompt}]}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return {"answer": response.json()["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}