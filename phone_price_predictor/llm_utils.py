from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

_client = OpenAI(
    base_url=os.getenv("MLAPI_BASE_URL"),
    api_key=os.getenv("MLAPI_API_KEY")
)


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        response = _client.chat.completions.create(
            model="openai/gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_completion_tokens=2000
        )
        content = response.choices[0].message.content
        if not content:
            return "⚠️ AI가 빈 응답을 반환했습니다."
        return content
    except Exception as e:
        return f"⚠️ AI 설명 생성 중 오류가 발생했습니다: {e}"