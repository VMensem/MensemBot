#!/usr/bin/env python3
import os
import asyncio
import threading
from flask import Flask, Response

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# ================== Конфиг ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CREATOR_ID = 1951437901

admins = set([CREATOR_ID])
texts = {
    "start": """👋 Привет! Я MensemBot.
ℹ️ Информация - /info
📜 Правила - /rules
📊 Цены на ранги - /rank
✅ Остальные команды - /help

🛡Discord сервер: https://mensem.fun/discord
🎀 Общий чат: https://t.me/mensem_barone
📕Barone Family: https://t.me/baronefam
📘Mensem Club: https://t.me/+sl5f-AkJBmFiZjgy
    """,
    "info": """ℹ️ Информация
👋Привет, данный бот создан специально для 📙Barone Family и 📘Mensem Club
✅ Создатель бота и семей - @vladlotto - обращайтесь к нему по всем вопросам!

🛡Discord сервер: https://mensem.fun/discord
🎀 Общий чат: https://t.me/mensem_barone
📕Barone Family: https://t.me/baronefam
📘Mensem Club: https://t.me/+sl5f-AkJBmFiZjgy

💂‍♂️Лидеры: @Sergei_Chapaev / @DoneBarone
🥷Заместители:  @Santa_Chapaev / @Cobalt228 / @vladlotto / @Paradise_Lin / @Studenticks
    """,
    "rank": """📊 Цены на ранги 
    💵Barone Family:
2  - 2кк либо вступить в группу
3 - 3кк
4 - 4кк
5 - 5кк или фулл випка ( адд и премка ), либо промокод
6 - 6кк
7 - 7кк
8 - 8кк либо смена ника на Barone или Mensem
💶Mensem Club:
3 - 3кк
4 - 4кк
5 - 5кк или  промокод
6 - 6кк
7 - Есле есть адд или премиум вип
8 - Долго находится в фаме или сменить ник на Mensem
""",
    "rules": """📜 Правила
Первое и самое главное правило!
Если хоть 1 пидарас из вас напишет какую-то хуету, сразу в ЧСФ
p.s. Дальше сами думайте кикие правила делать!
""",
    "help": """❓ Доступные команды: 
🧩 /help - Команды
✅ /start - Запуск Бота
ℹ️ /info - Информация
📜 /rules - Правила
📊 /rank - Цены на ранги
💵 /shop - Купить ранг
🆔 /id - Посмотреть свой ID
🎀 /idea - Отправить идею/жалобу руководству
""",
    "shop": """Чтобы подать заявку на ранг
Вам нужно отправить фото(скриншот) того как вы пополнили семейный счёт на определённую сумму из /rank
И в подпись к фото добавить текст

Пример:
Ник: Vlad_Mensem
Семья: Mensem
Ранг: 5
Док-ва: Скриншот пополнения счёта
""",
}
idea_chat_id = "-1002473077041"

# ================== Flask ==================
health_app = Flask(__name__)

@health_app.route("/", methods=["GET"])
def index():
    return Response("✅MensemBot - успешно запущен, и работает 24/7", mimetype="text/plain")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    health_app.run(host="0.0.0.0", port=port)

# ================== Бот ==================
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ================== Helpers ==================
def isCreator(user_id: int) -> bool:
    return user_id == CREATOR_ID

def isAdmin(user_id: int) -> bool:
    return user_id in admins

def get_user_display(user: types.User) -> str:
    return f"{user.full_name} (@{user.username})" if user.username else user.full_name

# ================== Основные команды ==================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(texts["start"])

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(texts["info"])

@dp.message(Command("rank"))
async def cmd_rank(message: types.Message):
    await message.answer(texts["rank"])

@dp.message(Command("rules"))
async def cmd_rules(message: types.Message):
    await message.answer(texts["rules"])

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(texts["help"])

@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    await message.answer(f"Ваш ID: <code>{message.from_user.id}</code>")

# ================== Админские команды ==================
async def set_text_cmd(message: types.Message, key: str):
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ Недостаточно прав.")
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return await message.answer("⚠️ Укажи текст.")
    texts[key] = parts[1]
    await message.answer(f"✅ {key} обновлён.")

@dp.message(Command("setstart"))
async def cmd_setstart(message: types.Message):
    await set_text_cmd(message, "start")

@dp.message(Command("setinfo"))
async def cmd_setinfo(message: types.Message):
    await set_text_cmd(message, "info")

@dp.message(Command("setrank"))
async def cmd_setrank(message: types.Message):
    await set_text_cmd(message, "rank")

@dp.message(Command("setrules"))
async def cmd_setrules(message: types.Message):
    await set_text_cmd(message, "rules")

@dp.message(Command("sethelp"))
async def cmd_sethelp(message: types.Message):
    await set_text_cmd(message, "help")

@dp.message(Command("setshop"))
async def cmd_setshop(message: types.Message):
    await set_text_cmd(message, "shop")

@dp.message(Command("setideachat"))
async def cmd_setideachat(message: types.Message):
    global idea_chat_id
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ Недостаточно прав.")
    parts = message.text.split(" ", 1)
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("⚠️ Укажи ID чата.")
    idea_chat_id = int(parts[1])
    await message.answer(f"✅ Чат идей обновлён: {idea_chat_id}")

@dp.message(Command("addadmin"))
async def cmd_addadmin(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Только создатель может добавлять админов.")
    if not message.reply_to_message:
        return await message.answer("⚠️ Ответь на сообщение пользователя, чтобы выдать админку.")
    uid = message.reply_to_message.from_user.id
    admins.add(uid)
    await message.answer(f"✅ {get_user_display(message.reply_to_message.from_user)} теперь админ.")

@dp.message(Command("unadmin"))
async def cmd_unadmin(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Только создатель может снимать админку.")
    if not message.reply_to_message:
        return await message.answer("⚠️ Ответь на сообщение пользователя, чтобы снять админку.")
    uid = message.reply_to_message.from_user.id
    if uid in admins:
        admins.remove(uid)
        await message.answer(f"❌ {get_user_display(message.reply_to_message.from_user)} больше не админ.")

@dp.message(Command("staff"))
async def cmd_staff(message: types.Message):
    staff_list = [f"👑 Создатель: {get_user_display(message.from_user) if message.from_user.id==CREATOR_ID else CREATOR_ID}"]
    for uid in admins:
        if uid != CREATOR_ID:
            try:
                user = await bot.get_chat(uid)
                staff_list.append(f"🔑 Админ: {get_user_display(user)}")
            except:
                staff_list.append(f"🔑 Админ: ID {uid}")
    await message.answer("\n".join(staff_list))

@dp.message(Command("botstats"))
async def cmd_botstats(message: types.Message):
    if not isCreator(message.from_user.id):
        return
    await message.answer(f"📊 Bot stats:\nAdmins: {len(admins)}\nIdeaChat: {idea_chat_id}")

# ================== /shop с фото ==================
@dp.message(Command("shop"))
async def cmd_shop(message: types.Message):
    if message.chat.type != "private":
        return await message.answer("⚠️ Магазин доступен только в личке с ботом.")
    await message.answer(texts["shop"])

@dp.message(F.photo)
async def handle_shop_order(message: types.Message):
    if message.chat.type != "private":
        return
    if not message.caption:
        return await message.answer("❌ Добавь подпись к фото (например: Ник: Vlad_Mensem, Семья: Mensem , Ранг: 5, Доказательства: Скрин).")
    if not idea_chat_id:
        return await message.answer("❌ Чат идей не настроен.")

    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Выдано", callback_data=f"approve:{message.from_user.id}")
    kb.button(text="❌ Отказано", callback_data=f"deny:{message.from_user.id}")

    await bot.send_photo(
        idea_chat_id,
        photo=message.photo[-1].file_id,
        caption=f"🛒 Новая заявка из /shop:\n\n{message.caption}\n\nОт: {get_user_display(message.from_user)}",
        reply_markup=kb.as_markup()
    )
    await message.answer("✅ Заявка отправлена руководству, ожидай ответа.")

# ================== Callbacks ==================
@dp.callback_query(F.data.startswith("approve"))
async def cb_approve(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await bot.send_message(user_id, "✅ Твоя заявка в /shop одобрена!")
    await callback.answer("Выдано!")

@dp.callback_query(F.data.startswith("deny"))
async def cb_deny(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await bot.send_message(user_id, "❌ Твоя заявка в /shop отклонена.")
    await callback.answer("Отказано!")

# ================== MAIN ==================
async def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
