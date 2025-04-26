import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from db import get_data, change_status, add_data, getAll

from config import bot_token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    msg = 'Список вещей на неделю\n\n'
    for key, value in getAll().items():
        msg = f'{msg}❕{value}. Куплено - /buyed{key}\n'
    await message.reply(msg)


# todo: тут сделать хэндлер проверяющий префикс команды, равна ли она add. Из суфикса команды вытаскивается срок: week, month, year
@dp.message(Command("add"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")

# todo: тут сделать хэндлер проверяющий префикс команды, равна ли она buyed. Из суфикса команды вытаскивается срок: week, month, year
@dp.message(Command("buyed"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())