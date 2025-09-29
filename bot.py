import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

# ======= НАСТРОЙКИ =======
TOKEN = "8170191285:AAFu9e0VGeeJYjYbTTaenuMeiT6zZTyVliQ"  # вставь токен бота
CREATOR_ID = 1951437901    # твой Telegram ID

# ======= НАСТРОЙКА ЛОГОВ =======
logging.basicConfig(level=logging.INFO)

# ======= СОЗДАНИЕ БОТА =======
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ======= ДАННЫЕ =======
data = {
    "start": "Привет! Я бот 😊",
    "info": "Информация о боте.",
    "rules": "Правила ещё не установлены.",
    "rank": "У тебя обычный ранг.",
    "admins": set(),   # список админов
}

# ======= ФУНКЦИИ ПРОВЕРОК =======
def isCreator(user_id: int) -> bool:
    return user_id == CREATOR_ID

def isAdmin(user_id: int) -> bool:
    return user_id == CREATOR_ID or user_id in data["admins"]

# ======= ОБРАБОТЧИКИ КОМАНД =======

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(data["start"])

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(data["info"])

@dp.message(Command("rules"))
async def cmd_rules(message: types.Message):
    await message.answer(data["rules"])

@dp.message(Command("rank"))
async def cmd_rank(message: types.Message):
    await message.answer(data["rank"])

@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    await message.answer(f"Твой ID: <code>{message.from_user.id}</code>")

@dp.message(Command("setstart"))
async def cmd_setstart(message: types.Message):
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ Нет доступа")
    text = message.text.split(" ", 1)
    if len(text) > 1:
        data["start"] = text[1]
        await message.answer("✅ Сообщение /start изменено.")
    else:
        await message.answer("❌ Использование: /setstart <текст>")

@dp.message(Command("setinfo"))
async def cmd_setinfo(message: types.Message):
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ Нет доступа")
    text = message.text.split(" ", 1)
    if len(text) > 1:
        data["info"] = text[1]
        await message.answer("✅ Сообщение /info изменено.")
    else:
        await message.answer("❌ Использование: /setinfo <текст>")

@dp.message(Command("setrules"))
async def cmd_setrules(message: types.Message):
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ Нет доступа")
    text = message.text.split(" ", 1)
    if len(text) > 1:
        data["rules"] = text[1]
        await message.answer("✅ Сообщение /rules изменено.")
    else:
        await message.answer("❌ Использование: /setrules <текст>")

@dp.message(Command("setrank"))
async def cmd_setrank(message: types.Message):
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ Нет доступа")
    text = message.text.split(" ", 1)
    if len(text) > 1:
        data["rank"] = text[1]
        await message.answer("✅ Сообщение /rank изменено.")
    else:
        await message.answer("❌ Использование: /setrank <текст>")

@dp.message(Command("shop"))
async def cmd_shop(message: types.Message):
    await message.answer("🛒 Магазин скоро будет доступен!")

@dp.message(Command("idea"))
async def cmd_idea(message: types.Message):
    text = message.text.split(" ", 1)
    if len(text) > 1:
        await message.answer(f"💡 Идея принята: {text[1]}")
    else:
        await message.answer("❌ Использование: /idea <ваша идея>")

@dp.message(Command("staff"))
async def cmd_staff(message: types.Message):
    admins_list = [str(uid) for uid in data["admins"]]
    await message.answer(
        f"👑 Создатель: <code>{CREATOR_ID}</code>\n"
        f"🛡 Админы: {', '.join(admins_list) if admins_list else 'нет'}"
    )

@dp.message(Command("addadmin"))
async def cmd_addadmin(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Только создатель может добавлять админов.")
    text = message.text.split(" ", 1)
    if len(text) > 1 and text[1].isdigit():
        uid = int(text[1])
        data["admins"].add(uid)
        await message.answer(f"✅ Пользователь {uid} добавлен в админы.")
    else:
        await message.answer("❌ Использование: /addadmin <user_id>")

@dp.message(Command("unadmin"))
async def cmd_unadmin(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Только создатель может удалять админов.")
    text = message.text.split(" ", 1)
    if len(text) > 1 and text[1].isdigit():
        uid = int(text[1])
        if uid in data["admins"]:
            data["admins"].remove(uid)
            await message.answer(f"✅ Пользователь {uid} удалён из админов.")
        else:
            await message.answer("❌ Этот пользователь не админ.")
    else:
        await message.answer("❌ Использование: /unadmin <user_id>")

@dp.message(Command("botstats"))
async def cmd_botstats(message: types.Message):
    await message.answer("📊 Статистика бота: пока пусто 🙂")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "<b>Доступные команды:</b>\n"
        "/start – стартовое сообщение\n"
        "/info – информация\n"
        "/rules – правила\n"
        "/rank – твой ранг\n"
        "/shop – магазин\n"
        "/id – показать твой ID\n"
        "/idea <текст> – предложить идею\n"
        "/staff – список админов\n"
        "/botstats – статистика бота\n\n"
        "<b>Команды для админов:</b>\n"
        "/setstart <текст>\n/setinfo <текст>\n/setrules <текст>\n/setrank <текст>\n\n"
        "<b>Команды для создателя:</b>\n"
        "/addadmin <id>\n/unadmin <id>"
    )

# ======= ЗАПУСК =======
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
