from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from dotenv import load_dotenv
import requests 

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific frontend origin for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


@app.post("/product")
async def send_message(request: Request):
    data = await request.json()
    
    tg_id = data.get("tg_id")
    name = data.get("name")
    category = data.get("category")

    if not tg_id or not name or not category:
        return {"error": "Missing required fields in request"}

    message = f"Вы выбрали товар: {name}\nВ категории: {category}"


    # Inline keyboard markup with two buttons
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "📞 Связаться с нами", "url": "https://wa.me/79854576117"}
            ],
            [
                {"text": "🌐 Наш сайт", "url": "https://belsi-home.ru/"}
            ],  
        ]
    }

    payload = {
        "chat_id": tg_id,
        "text": message,
        "reply_markup": reply_markup,
        "parse_mode": "HTML"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TELEGRAM_API_URL,
            json=payload
        )

@app.post("/")
async def handle_update(request: Request):
    update = await request.json()


    # Safely extract text message
    message = update.get("message", {})
    text = message.get("text")
    chat = message.get("chat", {})
    chat_id = chat.get("id")

    if text == "/start" and chat_id:
        send_message(chat_id, "Привет! На связи BELSI Kids. У нас есть широкий выбор стильной и безопасной мебели для детей ДОУ и школьных учреждений.")
    return {"ok": True}

def send_message(chat_id: int, text: str):
    url = f"{TELEGRAM_API_URL}"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📋 Меню",
                        "web_app": {
                            "url": "https://shumilovsergey.github.io/furniture/"
                        }
                    }

                ],
                [
                    {
                        "text": "📞 Связаться с нами",
                        "url": "https://belsi-home.ru/"
                    }
                ]
            ]
        }
    }

    try:
        response = requests.post(url, json=payload)
    except Exception as e:
        print('error')