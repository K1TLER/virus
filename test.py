from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
import asyncio
import os

API_TOKEN = os.getenv("BOT_TOKEN") or "8294968284:AAETRkaEUP84gTIPUJQrp9fyLoFTE0bL9hs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 36 карт (6–A) всех мастей в виде эмодзи
cards = [
    "🂦", "🂧", "🂨", "🂩", "🂪", "🂫", "🂭", "🂮",  # ♠
    "🂶", "🂷", "🂸", "🂹", "🂺", "🂻", "🂽", "🂾",  # ♥
    "🃆", "🃇", "🃈", "🃉", "🃊", "🃋", "🃍", "🃎",  # ♦
    "🃖", "🃗", "🃘", "🃙", "🃚", "🃛", "🃝", "🃞",  # ♣
]

CARD_TOTAL = len(cards)

# Хранение состояния для пользователей
user_states = {}

# Генерация клавиатуры
def get_keyboard(checked: set[int] = set()) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(CARD_TOTAL):
        text = "✅" if i in checked else cards[i]
        builder.button(text=text, callback_data=f"card:{i}")
    builder.adjust(6)
    builder.button(text="🔄 Сброс", callback_data="reset")
    return builder.as_markup()

# Обработка /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    user_states[message.chat.id] = set()
    await message.answer("🃏 Выберите карты:", reply_markup=get_keyboard())

# Обработка выбора карты
@dp.callback_query(F.data.startswith("card:"))
async def card_handler(callback: CallbackQuery):
    user_id = callback.message.chat.id
    card_index = int(callback.data.split(":")[1])
    state = user_states.setdefault(user_id, set())

    if card_index in state:
        state.remove(card_index)
    else:
        state.add(card_index)

    await callback.message.edit_reply_markup(reply_markup=get_keyboard(state))
    await callback.answer()

# Обработка сброса
@dp.callback_query(F.data == "reset")
async def reset_handler(callback: CallbackQuery):
    user_states[callback.message.chat.id] = set()
    await callback.message.edit_reply_markup(reply_markup=get_keyboard())
    await callback.answer("Все карты сброшены")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
