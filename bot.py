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
# ================== Flask ==================
health_app = Flask(__name__)
CORS(health_app)  # ✅ Разрешаем запросы с других доменов

@health_app.route("/", methods=["GET"])
def index():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot • Статус</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                height: 100vh;
                background: radial-gradient(circle at top, #200, #000);
                color: #fff;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .glow {
                font-size: 3em;
                font-weight: 700;
                color: #ff1b1b;
                text-shadow: 0 0 15px #ff1b1b, 0 0 40px #ff1b1b55;
                animation: pulse 2.5s infinite alternate;
            }
            @keyframes pulse {
                0% { text-shadow: 0 0 15px #ff1b1b, 0 0 30px #ff1b1b55; }
                100% { text-shadow: 0 0 35px #ff1b1b, 0 0 70px #ff1b1b99; }
            }
            .status-box {
                margin-top: 25px;
                padding: 15px 25px;
                border: 2px solid #ff1b1b66;
                border-radius: 10px;
                background: rgba(0, 0, 0, 0.35);
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
            }
            .status { font-size: 1.2em; color: #ccc; margin-top: 10px; }
            .pulse-dot {
                display: inline-block;
                width: 12px;
                height: 12px;
                background: #ff1b1b;
                border-radius: 50%;
                box-shadow: 0 0 10px #ff1b1b;
                animation: blink 1.5s infinite;
            }
            @keyframes blink {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.3; transform: scale(0.7); }
            }
            footer { position: absolute; bottom: 15px; font-size: 0.9em; color: #777; }
            a { color: #ff4747; text-decoration: none; transition: 0.3s; }
            a:hover { color: #fff; text-shadow: 0 0 8px #ff1b1b; }
        </style>
    </head>
    <body>
        <h1 class="glow">🔥 Робот Активен</h1>
        <div class="status-box">
            <p class="status">Состояние: <span class="pulse-dot"></span> Работает 24/7</p>
            <p>Проверка соединения выполнена успешно.</p>
        </div>
        <footer>© 2025 <a href="https://mensem.fun" target="_blank">Mensem.Fun</a> — by Vladyslav</footer>
    </body>
    </html>
    """

# 🔍 Технический эндпоинт для проверки состояния (для сайта Mensem.Fun)
@health_app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "bot": "MensemBot"}), 200

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

#============ Мут командс
from datetime import timedelta

def parse_duration(duration_str: str) -> timedelta:
    """Парсит строку формата '10m', '2h', '1d'"""
    try:
        num = int(''.join(filter(str.isdigit, duration_str)))
        if "h" in duration_str:
            return timedelta(hours=num)
        elif "d" in duration_str:
            return timedelta(days=num)
        else:
            return timedelta(minutes=num)
    except:
        return timedelta(minutes=10)  # по умолчанию 10 минут

@dp.message(Command("mute"))
async def cmd_mute(message: types.Message):
    if not message.chat.type.endswith("group"):
        return await message.answer("⚠️ Команда доступна только в группах.")
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ У тебя нет прав на использование этой команды.")
    if not message.reply_to_message:
        return await message.answer("⚠️ Ответь на сообщение пользователя, чтобы замутить его.")

    args = message.text.split()
    duration = parse_duration(args[1]) if len(args) > 1 else timedelta(minutes=10)
    until_date = message.date + duration
    user_id = message.reply_to_message.from_user.id

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=types.ChatPermissions(can_send_messages=False),
            until_date=until_date
        )

        time_str = (
            f"{duration.days} дн." if duration.days > 0 else
            f"{duration.seconds // 3600} ч." if duration.seconds >= 3600 else
            f"{duration.seconds // 60} мин."
        )
        await message.answer(
            f"🔇 Пользователь {message.reply_to_message.from_user.mention_html()} замучен на {time_str}.",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при попытке замутить: {e}")

@dp.message(Command("unmute"))
async def cmd_unmute(message: types.Message):
    if not message.chat.type.endswith("group"):
        return await message.answer("⚠️ Команда доступна только в группах.")
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ У тебя нет прав на использование этой команды.")
    if not message.reply_to_message:
        return await message.answer("⚠️ Ответь на сообщение пользователя, чтобы размутить его.")

    user_id = message.reply_to_message.from_user.id
    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=types.ChatPermissions(can_send_messages=True)
        )
        await message.answer(
            f"🔊 Пользователь {message.reply_to_message.from_user.mention_html()} размучен.",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при размуте: {e}")

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
