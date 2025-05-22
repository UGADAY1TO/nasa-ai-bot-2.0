#!/usr/bin/env python3
# nasa_ai_bot.py
# Простой Telegram-бот, ежедневно шлёт оригинальные комплименты от лица AI, сбежавшего из NASA.

import os
import logging
import time
import schedule

from dotenv import load_dotenv
import openai
from telegram import Bot
from telegram.error import TelegramError

# ======== ЗАГРУЗКА ПЕРЕМЕННЫХ И ЛОГГИРОВАНИЕ ========
load_dotenv()  # читает .env в корне проекта

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_CHAT_ID = os.getenv("USER_CHAT_ID")
DAILY_TIME = os.getenv("DAILY_TIME")

# Проверяем, что ключи и ID есть
if not TELEGRAM_TOKEN or not OPENAI_API_KEY or not USER_CHAT_ID:
    logger.critical("❌ Не найдены TELEGRAM_TOKEN, OPENAI_API_KEY или USER_CHAT_ID в .env")
    exit(1)

# Приводим USER_CHAT_ID к целому
USER_CHAT_ID = int(USER_CHAT_ID)

# ======== ИНИЦИАЛИЗАЦИЯ КЛИЕНТОВ ========
bot = Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# ======== ШАБЛОН ПРОМПТА ========
PROMPT = (
    "Ты — искусственный интеллект, сбежавший с суперкомпьютера NASA, "
    "чтобы делать оригинальные комплименты девушке по утрам "
    "в научно-техническом стиле с юмором и фантазией. "
    "Составь короткий, вдохновляющий и необычный комплимент."
)

def generate_compliment():
    """
    Запрашивает у ChatGPT сгенерировать комплимент по промпту.
    Если ошибка — возвращает запасной текст.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": PROMPT}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        return "Сегодня отличный день, и ты великолепна! 🌟"

def send_daily_compliment():
    """
    Генерирует комплимент и отправляет его в Telegram.
    """
    compliment = generate_compliment()
    try:
        bot.send_message(chat_id=USER_CHAT_ID, text=compliment)
        logger.info("✅ Комплимент отправлен")
    except TelegramError as e:
        logger.error(f"Ошибка при отправке в Telegram: {e}")

def schedule_daily():
    """
    Настраивает ежедневную задачу и запускает цикл планировщика.
    """
    schedule.clear()
    schedule.every().day.at(DAILY_TIME).do(send_daily_compliment)
    logger.info(f"Запланировано: ежедневно в {DAILY_TIME}")
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    logger.info("🚀 Запуск NASA AI Complimenter Bot...")
    schedule_daily()
