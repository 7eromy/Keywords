import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import gspread

# Установите токен вашего бота и ваш Telegram ID
BOT_TOKEN = "7236570390:AAEqOVlafSKKEJTU3WlP6SrpksIgxNRM88M"
ADMIN_ID = 1678720802

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
        sheet = gc.open_by_url(
            "https://docs.google.com/spreadsheets/d/1JU6OYcW0qSLO5QHIrzy_FfFqoiKcwGshjuuY3tanQDE/edit?gid=0")
        worksheet = sheet.get_worksheet(1)
        worksheet.append_row([message_text])
    except Exception as e:
        logging.error(f"Ошибка при записи сообщения в Google таблицу: {e}")


# Обработчик сообщений в группе
@dp.message()
async def keyword_handler(message: Message):
    KEYWORDS = get_keywords_from_google_sheet()
    message_text = message.text.lower()
    found_keywords = [keyword for keyword in KEYWORDS if keyword in message_text]

    if found_keywords:
        write_message_to_google_sheet(message.text)
        await bot.send_message(
            ADMIN_ID,
            f"Найдено сообщение с ключевыми словами:\n{message.text}"
        )
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

