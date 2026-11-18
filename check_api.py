import requests

print("正在向本地 FastAPI 发送请求...")
try:
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"prompt": "你好，请用一句话介绍你自己"},
        timeout=30
    )
    print(f"✅ 本地接口响应码: {response.status_code}")
    print(f"🤖 AI 的回答: {response.json()}")
except Exception as e:
    print(f"❌ 请求失败，报错: {e}")