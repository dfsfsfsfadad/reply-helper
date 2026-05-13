import base64
import json
import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
from groq import Groq

app = FastAPI()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

@app.get("/", response_class=HTMLResponse)
async def root():
    html = Path("templates/index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.post("/analyze")
async def analyze(
    text: str = Form(default=""),
    image: UploadFile = File(default=None)
):
    client = Groq(api_key=GROQ_API_KEY)

    content = []

    if image and image.filename:
        image_data = await image.read()
        b64 = base64.standard_b64encode(image_data).decode("utf-8")
        media_type = image.content_type or "image/jpeg"
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{media_type};base64,{b64}"}
        })

    prompt_parts = []
    if text:
        prompt_parts.append(f"Переписка:\n{text}")
    if image and image.filename:
        prompt_parts.append("(также прикреплён скриншот переписки выше)")

    prompt_parts.append("""
На основе этой переписки сгенерируй ровно 4 варианта ответа.

Верни ответ СТРОГО в формате JSON (без лишнего текста, без markdown):
{
  "variants": [
    {"style": "Дружеский 😊", "text": "..."},
    {"style": "С юмором 😄", "text": "..."},
    {"style": "С намёком 😏", "text": "..."},
    {"style": "С иронией 🙃", "text": "..."}
  ]
}
""")

    content.append({"type": "text", "text": "\n\n".join(prompt_parts)})

    model = "meta-llama/llama-4-scout-17b-16e-instruct" if (image and image.filename) else "llama-3.3-70b-versatile"

    response = client.chat.completions.create(
        model=model,
        max_tokens=1500,
        messages=[{"role": "user", "content": content}]
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    data = json.loads(raw)
    return JSONResponse(content=data)
