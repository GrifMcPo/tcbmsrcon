import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import mcrcon
import config

# ===== НАСТРОЙКИ ИЗ CONFIG.PY =====
TOKEN = config.kwargs['token']
ADMIN_ID = int(config.kwargs['admins_list'][0])
RCON_HOST = config.kwargs['rcon_host'].split(':')[0]
RCON_PORT = int(config.kwargs['rcon_host'].split(':')[1]) if ':' in config.kwargs['rcon_host'] else 25575
RCON_PASS = config.kwargs['rcon_pass']
# ===================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def send_rcon(command: str) -> str:
    """Отправляет команду на сервер через RCON"""
    try:
        with mcrcon.MCRcon(RCON_HOST, RCON_PASS, port=RCON_PORT) as m:
            resp = m.command(command)
            return resp if resp else "✅ Команда выполнена"
    except Exception as e:
        return f"❌ Ошибка RCON: {e}"

# ===== КОМАНДЫ =====

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "🤖 **Бот управления Minecraft сервером**\n\n"
        "📋 **Команды:**\n"
        "/online — список игроков онлайн\n"
        "/say <текст> — сообщение в чат сервера\n"
        "/ban <ник> — забанить игрока\n"
        "/unban <ник> — разбанить игрока\n"
        "/cmd <команда> — выполнить любую консольную команду\n"
        "/help — показать это сообщение",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await start_cmd(message)

@dp.message(Command("online"))
async def online_cmd(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return
    resp = send_rcon("list")
    await message.answer(f"📊 **Игроки онлайн:**\n`{resp}`", parse_mode="Markdown")

@dp.message(Command("say"))
async def say_cmd(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return
    text = message.text.replace("/say", "", 1).strip()
    if not text:
        await message.answer("❌ Напишите: `/say Привет всем!`", parse_mode="Markdown")
        return
    resp = send_rcon(f"say {text}")
    await message.answer(f"💬 **Сообщение отправлено:**\n`{resp}`", parse_mode="Markdown")

@dp.message(Command("ban"))
async def ban_cmd(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return
    nick = message.text.replace("/ban", "", 1).strip()
    if not nick:
        await message.answer("❌ Укажите ник: `/ban Player`", parse_mode="Markdown")
        return
    resp = send_rcon(f"ban {nick}")
    await message.answer(f"🔨 **Игрок {nick} забанен:**\n`{resp}`", parse_mode="Markdown")

@dp.message(Command("unban"))
async def unban_cmd(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return
    nick = message.text.replace("/unban", "", 1).strip()
    if not nick:
        await message.answer("❌ Укажите ник: `/unban Player`", parse_mode="Markdown")
        return
    resp = send_rcon(f"pardon {nick}")
    await message.answer(f"🔓 **Игрок {nick} разбанен:**\n`{resp}`", parse_mode="Markdown")

@dp.message(Command("cmd"))
async def cmd_cmd(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return
    command = message.text.replace("/cmd", "", 1).strip()
    if not command:
        await message.answer("❌ Укажите команду: `/cmd say Hello`", parse_mode="Markdown")
        return
    resp = send_rcon(command)
    await message.answer(f"⚙️ **Команда выполнена:**\n`{resp}`", parse_mode="Markdown")

# ===== ОСТАЛЬНЫЕ СООБЩЕНИЯ =====

@dp.message()
async def fallback(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("❓ Неизвестная команда. Используйте /start для списка.")
    else:
        await message.answer("⛔ У вас нет доступа к этому боту.")

# ===== ЗАПУСК =====

async def main():
    logging.info("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
