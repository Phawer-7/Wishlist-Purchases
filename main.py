import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject

from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import get_data, change_status, add_data, getAll

from config import bot_token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()

local = {
    "week": "hafta",
    "month": "oy"
}


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="За неделю", callback_data="week"))
    builder.add(types.InlineKeyboardButton(text="За месяц", callback_data="month"))
    await message.answer("Показать список необходимых покупок на неделю", reply_markup=builder.as_markup())


@dp.message(F.text.startswith('/buyed'))
async def buy_process(message: types.Message):
    id = int(message.text[6])
    change_status(id)
    name = get_data(id, data='name')
    type = get_data(id, data='type')

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Открыть список", callback_data=type))
    await message.answer(f"Продукт {name} куплен", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'week')
@dp.callback_query(F.data == 'month')
async def callback_processing(callback: types.CallbackQuery):
    msg = f'Список вещей на {local[callback.data]}\n\n'
    for key, value in getAll(type=callback.data).items():
        msg = f'{msg}❕{value}. Куплено - /buyed{key}\n'
    await callback.message.answer(msg)
    await callback.answer()


@dp.message(Command("add"))
async def adding_newproduct(message: types.Message, command: CommandObject):
    if command.args == None:
        await message.reply("Недопустимый формат")
    else:
        type = command.args.split()[0]
        if type in ['week', 'month']:
            name = " ".join(command.args.split()[1:])
            if not len(name) == 0:
                add_data(name, type)
                await message.reply(f"{name} добавлен в раздел {type}")
            else:
                await message.reply("Недопустимый формат")
        else:
            await message.reply("Недопустимый формат")


@dp.message(Command("test"))
async def testfunc(message: types.Message, command: CommandObject):
    pass


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
