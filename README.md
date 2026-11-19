# 🚀 AI 应用通用后端服务底座 (FastAPI + MySQL + JWT + LLM + Docker)

基于 FastAPI 构建的现代化、模块化后端服务。本项目从零搭建，涵盖分层架构、OAuth2 + JWT 用户认证、MySQL 持久化、DeepSeek 大模型 API 集成与 Docker 部署，具备完善的工业级开发规范。

## 🛠 技术栈
* **语言**: Python 3.12
* **后端框架**: FastAPI, SQLAlchemy, Pydantic
* **数据库**: MySQL 8.0
* **认证与安全**: OAuth2 + JWT (JSON Web Token), Passlib (Bcrypt 密码哈希)
* **AI 集成**: DeepSeek 大模型 API (HTTP 客户端调用)
* **测试与部署**: Pytest, Docker

## 📸 运行效果展示

### 1. OAuth2 身份认证
![授权截图](./assets/auth.png)

### 2. 用户信息鉴权隔离
![用户信息](./assets/user.png)

### 3. AI 大模型接口调用
![AI对话](./assets/chat1.png)
![AI对话](./assets/chat2.png)

### 4. Docker 容器化部署
![Docker运行](./assets/docker_run.png)

### 5. 接口联调测试
![接口测试](./assets/api_docs.png)

### 6. MySQL 数据持久化 (密码哈希存储)
![数据库](./assets/mysql.png)

## 📂 项目结构
```text
├── app/
│   ├── crud.py          # 数据库操作逻辑
│   ├── database.py      # MySQL 连接与 ORM 配置
│   ├── main.py          # 路由入口与 API (含依赖注入)
│   ├── models.py        # SQLAlchemy 数据表模型
│   ├── schemas.py       # Pydantic 参数校验
│   └── security.py      # JWT 生成与密码哈希逻辑
├── test_main.py         # 自动化接口测试
├── requirements.txt     # 依赖清单
├── Dockerfile           # 容器构建文件
└── README.md
🚀 快速启动指南

1. 环境准备

建议使用虚拟环境运行：

```bash
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt
```

2. 配置环境变量 (安全规范)

本项目采用环境变量管理敏感信息，请勿将真实密钥硬编码或提交至版本库。
在项目根目录新建 .env 文件，填入以下配置：

```env
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/fastapi_demo
DEEPSEEK_API_KEY=sk-your_deepseek_api_key
SECRET_KEY=your_jwt_secret_key
```

3. 启动服务

```bash
uvicorn app.main:app --reload
```

访问 Swagger 文档：http://127.0.0.1:8000/docs

🧪 自动化测试

```bash
pytest test_main.py -v
```

💡 技术难点与解决方案

1. 容器网络隔离：在 Docker 容器内使用 127.0.0.1 无法访问宿主机 MySQL。通过在 database.py 中配置动态环境变量，在容器内切换至 host.docker.internal，成功打通内外网通信。
2. 安全鉴权：摒弃基础的 Session 机制，采用 OAuth2 + JWT 无状态鉴权。自定义 get_current_user 依赖注入函数，全局拦截未授权访问。
3. 测试环境污染：在 Pytest 中通过 app.dependency_overrides 替换生产数据库依赖，接入 SQLite 内存数据库，确保每次测试环境纯净，避免脏数据。

```
