import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

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
    builder.add(types.InlineKeyboardButton(text="Bir haftalik", callback_data="week"))
    builder.add(types.InlineKeyboardButton(text="Bir oylik", callback_data="month"))
    await message.answer("🛒Sotib olish kerak bo'lgan narsalarni ko'rsatish...", reply_markup=builder.as_markup())


@dp.message(F.text.startswith('/buyed'))
async def buy_process(message: types.Message):
    id = int(message.text[6])
    change_status(id)
    name = get_data(id, data='name')
    type = get_data(id, data='type')

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Ro'yxatni ochish", callback_data=type))
    await message.answer(f"✅Mahsulot {name.title()} olindi", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'week')
@dp.callback_query(F.data == 'month')
async def callback_processing(callback: types.CallbackQuery):
    msg = f"{local[callback.data].title()}lik mahsulotlarni ro'yxati:\n\n"
    for key, value in getAll(type=callback.data).items():
        msg = f"{msg}❕{value.title()}. Olingan bo'lsa - /buyed{key}\n"
    await bot.edit_message_text(text=msg, chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.answer()


@dp.message(Command("help"))
async def get_help(message: types.Message):
    await message.reply("<b>Mahsulot qo'shish buyrug'i:</b>\n\n<code>/add [week/month] mahsulot nomi</code>\nMasalan: <code>/add week olma</code> - " \
    "olma degan mahsulotni haftalik ro'yxatga qo'shadi.", parse_mode=ParseMode.HTML)


@dp.message(Command("add"))
async def adding_newproduct(message: types.Message, command: CommandObject):
    if command.args == None:
        await message.reply("Yaroqsiz format")
    else:
        type = command.args.split()[0]
        if type in ['week', 'month']:
            name = " ".join(command.args.split()[1:])
            if not len(name) == 0:
                add_data(name, type)
                await message.reply(f"{name.title()} {local[type]}ga qo'shildi.")
            else:
                await message.reply("Yaroqsiz format")
        else:
            await message.reply("Yaroqsiz format")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
