import requests
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


@router.post("/chat")
def chat_with_ai(request: ChatRequest):
    # ⚠️ 把下面换成你的真实 Key
    API_KEY ="sk-你的Key填这里"

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
        answer = result["choices"][0]["message"]["content"]
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}