# ReplyAI — помощник в переписке 💬

Вставь скриншот или текст переписки → получи 4 варианта ответа.

## Запуск за 3 шага

### 1. Установи зависимости
```bash
pip install -r requirements.txt
```

### 2. Добавь API ключ
**На Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**На Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

> Ключ берёшь на https://console.anthropic.com

### 3. Запусти сервер
```bash
uvicorn main:app --reload
```

Открой браузер: **http://localhost:8000** 🚀

---

## Структура проекта
```
reply-helper/
├── main.py           ← FastAPI backend
├── requirements.txt  ← зависимости Python
├── templates/
│   └── index.html    ← интерфейс
└── README.md
```

## Что умеет
- 📸 Загрузка скриншота переписки (PNG, JPG, WEBP)
- 💬 Вставка текста переписки
- ✨ 4 варианта ответа: Дружеский, С юмором, С намёком, С иронией
- 📋 Кнопка «Копировать» для каждого варианта
