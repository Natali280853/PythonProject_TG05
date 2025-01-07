import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
from datetime import datetime, timedelta

from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Пишем функцию для получения случайного космического изображения дня (Astronomic Picture Of the Day = apod)
def get_random_apod():
    end_date = datetime.now()   # конечная дата - сегодня
    start_date = end_date - timedelta(days=365)  # Указываем начальную дату — за год до конечной даты
    random_date = start_date + (end_date - start_date) * random.random()  # random.random выдаёт случайное число от 0 до 1. 365 дней умножаются на дробное число, получается некое количество дней
    date_str = random_date.strftime("%Y-%m-%d")  # в этом формате, так написано в документации
    # Из документации берём ссылку и работаем с ней. Создаём переменную url внутри функции. Через эту переменную мы будем отправлять GET-запрос. Добавляем учёт и API-ключа, и даты (через &)
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'  # & = слиятние
    response = requests.get(url)  # Отправляем запрос и получаем JSON с ответом
    return response.json()


# Создаём команду, которая будет считывать, что мы хотим увидеть изображение. В круглых скобках указываем команду
@dp.message(Command("random_apod"))
# Создаём асинхронную функцию, которая будет брать всю информацию, полученную из переменной random_apod.
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']  # Отдельно сохраняем фото и заголовок
    title = apod['title']
    # Настраиваем отправку сообщения с фотографией и заголовком
    await message.answer_photo(photo=photo_url, caption=f"{title}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
