# 🚀 AI 应用通用后端服务底座 (FastAPI + MySQL + JWT + LLM + Docker)

基于 FastAPI 构建的现代化、模块化后端服务。本项目从零搭建，涵盖完整的分层架构、用户身份认证（OAuth2 + JWT）、MySQL 数据持久化、大语言模型（DeepSeek）集成，以及 Docker 容器化部署，具备完善的工业级开发规范与自动化测试体系。

## 🛠 技术栈
* **语言**: Python 3.12
* **后端框架**: FastAPI, SQLAlchemy, Pydantic
* **数据库**: MySQL 8.0
* **认证与安全**: OAuth2 + JWT (JSON Web Token), Passlib (Bcrypt 密码哈希)
* **AI 集成**: DeepSeek 大模型 API (HTTP 客户端调用)
* **测试与部署**: Pytest (独立内存数据库隔离), Docker

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
🔐 核心功能设计

1. 用户注册与安全存储：严格校验邮箱格式，用户密码采用 Bcrypt 算法进行单向哈希加密后入库，杜绝明文存储风险。
2. OAuth2 + JWT 鉴权：实现标准的登录签发 Token 流程，通过自定义 get_current_user 依赖注入，实现接口权限拦截与用户数据隔离。
3. AI 大模型接入：封装 /chat 受保护接口，通过 HTTP 协议与 DeepSeek API 交互，打通后端与大模型能力。
4. 容器化交付：编写 Dockerfile，解决容器网络隔离问题（通过 host.docker.internal 打通宿主机 MySQL），实现一键部署。

📸 运行效果展示

1. OAuth2 身份认证 (Swagger 绿锁授权)

通过密码流获取 Token，解锁受保护接口
<img width="532" height="380" alt="d3c9091616775a9a3e86b5ce04f390d2" src="https://github.com/user-attachments/assets/88a9e12a-a5b1-4210-a5a7-0793c07ce7d9" />
2. 用户信息鉴权隔离（/users/me）
携带 Token 请求，系统自动解析当前用户身份
<img width="306" height="184" alt="用户信息鉴权隔离" src="./assets/user_me.png">
3. AI 大模型接口调用（/chat）
携带 JWT 请求头，与 DeepSeek 大模型进行交互
<img width="909" height="428" alt="AI大模型接口调用" src="./assets/ai_chat_1.png">
<img width="740" height="208" alt="AI接口返回示例" src="./assets/ai_chat_2.png">

 4. Docker 容器化部署
镜像构建成功，容器处于 Up 运行状态，端口映射成功
<img width="851" height="169" alt="Docker容器部署" src="./assets/docker_run.png">

 5. 数据库持久化验证（密码加密存储）
用户信息成功写入 MySQL，密码字段已进行 Bcrypt 哈希加密
<img width="332" height="39" alt="数据库密码哈希存储" src="./assets/mysql_bcrypt.png">


---

本项目为个人全栈后端工程实践，旨在掌握 Python 现代 Web 开发与 AI 应用落地的全链路闭环。
