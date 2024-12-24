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
    "type": "service_account",
  "project_id": "keywords-445708",
  "private_key_id": "ceef495c0325c91fc457ffa8eddebff1708d7d6e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC046UEFZ+MyYqC\nA2pwcLcBjKmT0zXerUag/0R/8MJxsoj0NVn5yMVkybPTX7x/91CLMx7HXXzvqjeM\nI++C0SiZDb5mPphpIvvlPOrvCTMfp/EjJkZeAtCa6nrLGVojEdGOdKv6T8NPecxF\ntcG0ZUTyj+B52EXIm283L9tiA3MvhcIUho3ciOn4O992oPV02QJ+H1ISs4NKyAQf\nDriTB0pZv8nhUj5H+5BSo7AzISuuw/K7y7MbFdHJaHsabR6Z+b21Cvpt9sC366C/\nY+Md+1gJnZenrZS82/zOytzexAz5fPJUS7EcGvV3vCXFeUHMnZKTGeOjkehADnVg\nhL6I6VpBAgMBAAECggEAGb1I1l9zUBe/l0eAJlbLm7NVz/yebjyuz6rzJtdt+7rB\nZSqQToxEllZjOcEmM/lPozcXepvxcrMAa3cTlkRH6Bt+C9N9YXyCZni4H2JqPWdq\n1ysTmT4CTADwjyTg4Buhe4lbjWc7LfxxVjwKP66nVHKnqP7e0zBW733mVDiUc97x\nVYFBw7s69vOm12lJdwz9uHkjLdP+mjxbs7w1nXSp3Mand0M/miRHokz8gu2r0aAx\nG1z4VFJv4hw0PTgbb2T16600IuM2Zeh68mEWyzPl9jrsCx34wzI7Do4IhZmO3xks\n8eF+FImPf1hMFyaHn1cVL/D7EPPBzztgOJB+u+8U1wKBgQD2ShYtLQ2+WzS4YMD/\nUYN8x2gYmAXAPHcHIgA3xGRwRCzxmjsGIi2FEK14FXcyYIywPLXr/vyCAl5z7V6X\n5LCK4rHaHrRfX2aMM8JO1FFteVsmt+gFr8Bj0OhpKLl0k1xKICp4iSb+0qq4QTx/\ntcYxl1gzQKGA69vZ7uoenJH/1wKBgQC8BXGXhTgyYA4B7Y8Ck/ujZ1Rd+iG/NNUB\nNqcOTU3P0avt0NZFxEXEQHnh3YEpBaItaX4FHWxHSyzTu9m7hmbE3Eg/pKNRWhaC\nV43yVDavAPObOYiloCOJtQMFby/D/OB11BCIDzHyv8/D7APNY54rPwkvwATD+neN\nn57mIfWTpwKBgGWvPOy190Cqg1/EgqpnSzRPWAkfavBthm8peJGNwjIf07aEiO4F\nWmnf8t7rbeUcu7lft3SSOEqtE7YlQLLRtpoA8pEtsCbYSoyEKitFucDLI/keYOtI\nHtSXQf141OjulmH8WcyeQ71d2SJtvL61m/iJld7DRmrl9kVKQNsWpajNAoGAeiRX\nLIVggmkf8GSwuI4FtJsVlY8+iQX7MbSdRY82c0DUHcPCzsO4RstT4kSQ+WMtfa7A\nLPZ2NsJBNrMbuNSQwmYPkTiU1+5cHQRftAK9G2bU2gvAF0g2jejHM6qNLxaBgknn\nC1xDqFyuzanutmh2gcWLZDerYNy++YOuJ/X7oJUCgYAXtwv3z/U9NkyN+ztlHAvY\nQcoCtfOxf3fmD3bZUAvG43qKGBarZLzI59ZuLH/tJgMiPEzWg88cmCSSYkMYHpe+\nl38WywYPmjHy8W0rkykB5qYb2KxbY5g7ByEBg6hJD6m/OFXEoqwvuhAKfbiu3X1Z\nqF3b15RHfPS+J6fuhdOMJw==\n-----END PRIVATE KEY-----\n",
  "client_email": "keywords@keywords-445708.iam.gserviceaccount.com",
  "client_id": "112421599867897000722",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/keywords%40keywords-445708.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Функция для получения ключевых слов из Google таблицы
def get_keywords_from_google_sheet():
    try:
        gc = gspread.service_account_from_dict(credentials)
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JU6OYcW0qSLO5QHIrzy_FfFqoiKcwGshjuuY3tanQDE/edit?gid=0")
        worksheet = sheet.get_worksheet(0)
        keywords = worksheet.col_values(1)
        return [keyword.strip().lower() for keyword in keywords if keyword.strip()]
    except Exception as e:
        logging.error(f"Ошибка при получении ключевых слов из Google таблицы: {e}")
        return []

# Обработчик сообщений с текстом
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Бот запущен и отслеживает ключевые слова.")

@dp.message()
async def keyword_handler(message: Message):
    KEYWORDS = get_keywords_from_google_sheet()
    # Проверяем наличие ключевых слов
    message_words = set(message.text.lower().split())
    if any(keyword in message_words for keyword in KEYWORDS):
        await bot.send_message(
            ADMIN_ID,
            f"Найдено сообщение с ключевым словом:\n{message.text}"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

