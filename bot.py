#!/usr/bin/env python3
import os
import asyncio
import threading
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# ================== Конфиг ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CREATOR_ID = 1951437901
ADMIN_ID = CREATOR_ID

admins = set([CREATOR_ID])
idea_chat_id = -1002473077041

texts = {
    "start": """👋 Привет! Я MensemBot.
ℹ️ Информация - /minfo
📜 Правила - /mrules
📊 Цены на ранги - /mrank
✅ Остальные команды - /mhelp

🛡Discord сервер: https://mensem.fun/discord
🎀 Общий чат: https://t.me/mensem_barone
📕Barone Family: https://t.me/baronefam
📘Mensem Club: https://t.me/+sl5f-AkJBmFiZjgy
""",
    "info": """ℹ️ Информация
👋 Привет! Этот бот создан специально для 📙Barone Family и 📘Mensem Club.  
✅ Создатель бота и семей — @vladlotto  

🛡Discord сервер: https://mensem.fun/discord  
🎀 Общий чат: https://t.me/mensem_barone  
📕Barone Family: https://t.me/baronefam  
📘Mensem Club: https://t.me/+sl5f-AkJBmFiZjgy  

💂‍♂️Лидеры: @Sergei_Chapaev / @DoneBarone  
🥷Заместители: @Santa_Chapaev / @Cobalt228 / @vladlotto / @Paradise_Lin / @Studenticks
""",
    "rank": """📊 Цены на ранги 
💵Barone Family:
2 - 2кк либо вступить в группу
3 - 3кк
4 - 4кк
5 - 5кк или фулл випка (адд и премка), либо промокод
6 - 6кк
7 - 7кк
8 - 8кк либо смена ника на Barone или Mensem
💶Mensem Club:
3 - 3кк
4 - 4кк
5 - 5кк или промокод
6 - 6кк
7 - Если есть адд или премиум вип
8 - Долго в фаме или ник Mensem
""",
    "rules": """📜 Правила
Первое и самое главное правило!
Если хоть один напишет хуету — сразу ЧСФ.
p.s. Остальные правила решаем сами.
""",
    "help": """❓ Доступные команды: 
🧩 /mhelp — Команды
✅ /mstart — Запуск бота
ℹ️ /minfo — Информация
📜 /mrules — Правила
📊 /mrank — Цены на ранги
💵 /mshop — Купить ранг (в личке)
🆔 /mid — Посмотреть свой ID
🎀 /midea — Отправить идею/жалобу
""",
    "shop": """Чтобы подать заявку на ранг:
Отправь фото (скриншот) пополнения семейного счёта из /mrank  
и добавь подпись:

Ник: Vlad_Mensem  
Семья: Mensem  
Ранг: 5  
Док-ва: Скриншот пополнения счёта
"""
}

# ================== Flask ==================
health_app = Flask(__name__)
CORS(health_app)

@health_app.route("/", methods=["GET"])
def index():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MensemBot • Статус</title>
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
        <h1 class="glow">🔥 MensemBot Активен</h1>
        <div class="status-box">
            <p class="status">Состояние: <span class="pulse-dot"></span> Работает 24/7</p>
            <p>Проверка соединения выполнена успешно.</p>
        </div>
        <footer>© 2025 <a href="https://mensem.fun" target="_blank">Mensem.Fun</a> — by Vladyslav</footer>
    </body>
    </html>
    """

@health_app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "bot": "MensemBot"}), 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    health_app.run(host="0.0.0.0", port=port)

# ================== Telegram ==================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def isCreator(uid): return uid == CREATOR_ID
def isAdmin(uid): return uid in admins
def get_user_display(u): return f"{u.full_name} (@{u.username})" if u.username else u.full_name

# ================== Основные ==================
@dp.message(Command("mstart"))
async def start_cmd(m): await m.answer(texts["start"])

@dp.message(Command("minfo"))
async def info_cmd(m): await m.answer(texts["info"])

@dp.message(Command("mrank"))
async def rank_cmd(m): await m.answer(texts["rank"])

@dp.message(Command("mrules"))
async def rules_cmd(m): await m.answer(texts["rules"])

@dp.message(Command("mhelp"))
async def help_cmd(m): await m.answer(texts["help"])

@dp.message(Command("mid"))
async def id_cmd(m): await m.answer(f"Ваш ID: <code>{m.from_user.id}</code>")

# ================== Админские ==================
async def set_text_cmd(m, key):
    if not isAdmin(m.from_user.id): return await m.answer("❌ Недостаточно прав.")
    parts = m.text.split(" ", 1)
    if len(parts) < 2: return await m.answer("⚠️ Укажи текст.")
    texts[key] = parts[1]
    await m.answer(f"✅ {key} обновлён.")

for cmd, key in {
    "msetstart": "start",
    "msetinfo": "info",
    "msetrank": "rank",
    "msetrules": "rules",
    "msethelp": "help",
    "msetshop": "shop"
}.items():
    dp.message.register(lambda m, k=key: asyncio.create_task(set_text_cmd(m, k)), Command(cmd))

@dp.message(Command("maddadmin"))
async def addadmin(m):
    if not isCreator(m.from_user.id): return await m.answer("❌ Только создатель.")
    if not m.reply_to_message: return await m.answer("⚠️ Ответь на сообщение пользователя.")
    uid = m.reply_to_message.from_user.id
    admins.add(uid)
    await m.answer(f"✅ {get_user_display(m.reply_to_message.from_user)} теперь админ.")

@dp.message(Command("munadmin"))
async def unadmin(m):
    if not isCreator(m.from_user.id): return await m.answer("❌ Только создатель.")
    if not m.reply_to_message: return await m.answer("⚠️ Ответь на сообщение пользователя.")
    uid = m.reply_to_message.from_user.id
    if uid in admins:
        admins.remove(uid)
        await m.answer(f"❌ {get_user_display(m.reply_to_message.from_user)} снят с админов.")

@dp.message(Command("mstaff"))
async def staff(m):
    text = [f"👑 Создатель: {CREATOR_ID}"]
    for uid in admins:
        if uid != CREATOR_ID:
            text.append(f"🔑 Админ: {uid}")
    await m.answer("\n".join(text))

# ================== mute / unmute ==================
@dp.message(Command("mmute"))
async def mute_cmd(m):
    if not m.chat.type.endswith("group"): return await m.answer("⚠️ Только в группе.")
    if not isAdmin(m.from_user.id): return await m.answer("❌ Нет прав.")
    if not m.reply_to_message: return await m.answer("⚠️ Ответь на сообщение.")
    args = m.text.split()
    duration = timedelta(minutes=int(args[1].replace("m",""))) if len(args)>1 else timedelta(minutes=10)
    until_date = m.date + duration
    await bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id,
                                   permissions=types.ChatPermissions(can_send_messages=False),
                                   until_date=until_date)
    await m.answer("🔇 Замучен!")

@dp.message(Command("munmute"))
async def unmute_cmd(m):
    if not m.chat.type.endswith("group"): return await m.answer("⚠️ Только в группе.")
    if not isAdmin(m.from_user.id): return await m.answer("❌ Нет прав.")
    if not m.reply_to_message: return await m.answer("⚠️ Ответь на сообщение.")
    await bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id,
                                   permissions=types.ChatPermissions(can_send_messages=True))
    await m.answer("🔊 Размучен!")

# ================== /mshop ==================
@dp.message(Command("mshop"))
async def shop_cmd(m):
    if m.chat.type != "private": return await m.answer("⚠️ Только в личке.")
    await m.answer(texts["shop"])

@dp.message(F.photo)
async def photo_handler(m):
    if m.chat.type != "private": return
    if not m.caption: return await m.answer("⚠️ Добавь подпись.")
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Выдано", callback_data=f"approve:{m.from_user.id}")
    kb.button(text="❌ Отказано", callback_data=f"deny:{m.from_user.id}")
    await bot.send_photo(idea_chat_id, m.photo[-1].file_id,
                         caption=f"🛒 Новая заявка:\n\n{m.caption}\n\nОт: {get_user_display(m.from_user)}",
                         reply_markup=kb.as_markup())
    await m.answer("✅ Заявка отправлена руководству.")

@dp.callback_query(F.data.startswith("approve"))
async def cb_approve(cb):
    uid = int(cb.data.split(":")[1])
    await bot.send_message(uid, "✅ Твоя заявка одобрена!")
    await cb.answer("Выдано!")

@dp.callback_query(F.data.startswith("deny"))
async def cb_deny(cb):
    uid = int(cb.data.split(":")[1])
    await bot.send_message(uid, "❌ Твоя заявка отклонена.")
    await cb.answer("Отказано!")

# ================== MAIN ==================
async def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())