import asyncio
import logging
import re
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import gspread
from pymystem3 import Mystem

# Установите токен вашего бота и ваш Telegram ID
BOT_TOKEN = "7236570390:AAEqOVlafSKKEJTU3WlP6SrpksIgxNRM88M"
ADMIN_ID = 1678720802

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация Mystem
mystem = Mystem()

# Учетные данные для работы gspread
credentials = {
     # Здесь необходимо использовать учетные данные Google Cloud
}

# Функция для получения ключевых слов из Google таблицы
def get_keywords_from_google_sheet():
    try:
        gc = gspread.service_account_from_dict(credentials)
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JU6OYcW0qSLO5QHIrzy_FfFqoiKcwGshjuuY3tanQDE/edit?gid=0#gid=0")
        worksheet = sheet.get_worksheet(0)
        keywords = worksheet.col_values(1)
        return [keyword.strip().lower() for keyword in keywords if keyword.strip()]
    except Exception as e:
        logging.error(f"Ошибка при получении ключевых слов из Google таблицы: {e}")
        return []

# Функция для записи сообщения в Google таблицу
def write_message_to_google_sheet(message_text):
    try:
        gc = gspread.service_account_from_dict(credentials)
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JU6OYcW0qSLO5QHIrzy_FfFqoiKcwGshjuuY3tanQDE/edit?gid=0#gid=0")
        worksheet = sheet.get_worksheet(1)
        worksheet.append_row([message_text])
    except Exception as e:
        logging.error(f"Ошибка при записи сообщения в Google таблицу: {e}")

# Функция нормализации текста
def normalize_text(text):
    analysis = mystem.analyze(text)
    normalized_words = []
    for word in analysis:
        if "analysis" in word and word["analysis"]:
            normalized_words.append(word["analysis"][0]["lex"]) 
        elif "text" in word: 
            normalized_words.append(word["text"])
    return normalized_words

# Функция для лемматизации ключевых фраз
def normalize_keywords(keywords):
    return [" ".join(normalize_text(keyword)).strip() for keyword in keywords]

# Функция для поиска совпадений ключевых фраз
def find_exact_phrases(message_text, keywords):
    matches = []
    normalized_keywords = normalize_keywords(keywords)
    logging.info(f"Нормализованные ключевые слова: {normalized_keywords}")
    normalized_text = normalize_text(message_text)
    normalized_text_joined = " ".join(normalized_text).strip() 
    logging.info(f"Нормализованный текст: {normalized_text_joined}")

    for normalized_keyword in normalized_keywords:
        if re.search(rf'\b{re.escape(normalized_keyword)}\b', normalized_text_joined):
            matches.append(normalized_keyword)

    return matches

# Обработчик сообщений
@dp.message()
async def keyword_handler(message: Message):
    logging.info(f"Получено сообщение: {message.text}")
    KEYWORDS = get_keywords_from_google_sheet()
    logging.info(f"Ключевые слова: {KEYWORDS}")
    found_keywords = find_exact_phrases(message.text.lower(), KEYWORDS)
    logging.info(f"Найденные ключевые слова: {found_keywords}")

    if found_keywords:
        write_message_to_google_sheet(message.text)
        await bot.send_message(ADMIN_ID, f"Найдено сообщение с ключевыми словами:\n{message.text}")


# Основная функция
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
