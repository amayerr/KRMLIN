import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class UserForm(StatesGroup):
    name = State()
    age = State()

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="پروفایل",
                callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                text="تنظیمات",
                callback_data="settings"
            )
        ]
    ]
)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "ربات با موفقیت استارت شد چه کاری میتونم برات انجام بدم دوست من؟",
        reply_markup=start_keyboard
    )
@dp.callback_query(F.data == "profile")
async def profile_handler(callback):
    await callback.message.answer("این صفحه پروفایل شخضی شما میباشد: ")
    await callback.answer()
@dp.callback_query(F.data == "settings")
async def settings_handler(callback):
    await callback.message.answer("این صفحع تنظیمات حساب کاربری شما میباشد: ")
    await callback.answer()

@dp.message(Command("register"))
async def register(message: Message, state):
    await message.answer("لطفا برای ورود ابتدا اسم خود را بنویسید. . .")
    await state.set_state(UserForm.name)
@dp.message(UserForm.name)
async def get_name(message: Message, state):
    await state.update_data(name=message.text)
    await message.answer("لطفا سن خود را با دقت وارد کنید. . .")
    await state.set_state(UserForm.age)
@dp.message(UserForm.age)
async def get_age(message: Message, state):
    data = await state.get_data()
    name = data["name"]
    age = message.text
    await message.answer(
        f"کاربر {name} عزیز با {age} سال سن به پنل کاربری خوش امدید !"
    )
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())