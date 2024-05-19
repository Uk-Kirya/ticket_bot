import os
import random
from datetime import datetime

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
DB_PATH = os.getenv("DB_PATH")
AVIASALES_TOKEN = os.getenv("AVIASALES_TOKEN")

DEFAULT_COMMANDS = (
    ("start", "Найти билет 🔍"),
    ("about", "О боте 🤖"),
    ("help", "Помощь ℹ️")
)

greetings = {
    "good_morning": [
        "Доброе утро",
        "Добречко утречко",
        "С добрым утром"
    ],
    "good_day": [
        "Добрый день",
        "Добрейшего денечка",
        "Здравствуй"
    ],
    "good_evening": [
        "Вечер добрый",
        "Добрый вечер",
        "Добрейшего вечерочка"
    ],
    "good_night": [
        "Доброй ночи",
        "Наидобрейшей ночи",
        "С доброй ночью"
    ]
}

current_time = int(datetime.now().strftime("%H"))
if 8 <= current_time < 11:
    greeting = random.choice(greetings["good_morning"])
elif 18 <= current_time < 22:
    greeting = random.choice(greetings["good_evening"])
elif 22 <= current_time or current_time < 8:
    greeting = random.choice(greetings["good_night"])
else:
    greeting = random.choice(greetings["good_day"])
