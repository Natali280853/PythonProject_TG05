# Получите API ключ** на [RapidAPI](https://rapidapi.com/wirefreethought/api/geodb-cities/) для использования GeoDB.
from aiogram import Bot, Dispatcher, types
import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, RAPIDAPI_KEY
# Вставьте сюда ваш токен телеграм-бота и API-ключ для TheCatAPI


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Ваш RapidAPI ключ
RAPIDAPI_KEY = RAPIDAPI_KEY


# Функция для получения всех городов
def get_cities():
    url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all"
    headers = {
        'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com",
        'x-rapidapi-key': "cJvLRNK0GfdM9WSMbQe3inU7REn8JVy5"
    }
    response = requests.get(url, headers=headers)
    return response.json()


# Функция для получения информации о городе
def get_citi_info(city_name):
    cities = get_cities()
    for city in cities:
        if city['name'].lower() == city_name.lower():
            return city
    return None


# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот, который может предоставить информацию о городах. Используйте команду /city <название города> для получения информации.")


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот, который может предоставить информацию о городах. Используйте команду /city <название города> для получения информации.")


# Команда /city
@dp.message(Command("city"))
async def city(message: Message):
    try:
        city_name = message.text.split(" ", 1)[1]
    except IndexError:
        await message.answer("Пожалуйста, укажите название города.")
        return

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    querystring = {"namePrefix": city_name}
    headers = {
        'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            city_info = data['data'][0]  # Получаем первую подходящую запись
            city_details = f"Город: {city_info['name']}\n" \
                           f"Страна: {city_info['country']}\n" \
                           f"Широта: {city_info['latitude']}\n" \
                           f"Долгота: {city_info['longitude']}"
            await message.answer(city_details)
        else:
            await message.answer("Город не найден.")
    else:
        await message.answer("Произошла ошибка при запросе к API.")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

# В Telegram найдите своего бота и отправьте команду `/start` для начала работы.
# Используйте команду `/city <название города>` для получения информации о конкретном городе.

# Теперь у вас есть простой Telegram-бот, который использует API GeoDB для предоставления информации
# о городах. Вы можете расширять функционал, добавляя новые команды и возможности. Успехов в разработке!
