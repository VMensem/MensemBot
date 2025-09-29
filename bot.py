import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

# ======= НАСТРОЙКИ =======
TOKEN = "8170191285:AAFu9e0VGeeJYjYbTTaenuMeiT6zZTyVliQ"
CREATOR_ID = 1951437901   # твой Telegram ID

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
    "help": "Здесь список команд.",
    "shop": "Магазин временно недоступен.",
    "admins": set(),   # список админов
    "idea_chat": None, # чат для идей и заявок
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

# --- УСТАНОВКА ТЕКСТОВ ---
async def set_text(message: types.Message, key: str):
    if not isAdmin(message.from_user.id):
        return await message.answer("❌ Нет доступа")
    text = message.text.split(" ", 1)
    if len(text) > 1:
        data[key] = text[1]
        await message.answer(f"✅ Сообщение /{key} изменено.")
    else:
        await message.answer(f"❌ Использование: /set{key} <текст>", parse_mode=None)

@dp.message(Command("setstart"))
async def cmd_setstart(message: types.Message): await set_text(message, "start")

@dp.message(Command("setinfo"))
async def cmd_setinfo(message: types.Message): await set_text(message, "info")

@dp.message(Command("setrules"))
async def cmd_setrules(message: types.Message): await set_text(message, "rules")

@dp.message(Command("setrank"))
async def cmd_setrank(message: types.Message): await set_text(message, "rank")

@dp.message(Command("sethelp"))
async def cmd_sethelp(message: types.Message): await set_text(message, "help")

@dp.message(Command("setshop"))
async def cmd_setshop(message: types.Message): await set_text(message, "shop")

# --- УСТАНОВКА ЧАТА ДЛЯ ИДЕЙ ---
@dp.message(Command("setideachat"))
async def cmd_setideachat(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Только создатель может менять чат идей.")
    args = message.text.split()
    if len(args) == 2 and args[1].lstrip("-").isdigit():
        data["idea_chat"] = int(args[1])
        await message.answer(f"✅ Чат идей установлен: {args[1]}")
    else:
        await message.answer("❌ Использование: /setideachat <chat_id>")

# --- SHOP ---
@dp.message(Command("shop"))
async def cmd_shop(message: types.Message):
    if message.chat.type != "private":
        return await message.answer("❌ Использовать /shop можно только в личке с ботом.")
    await message.answer(
        f"{data['shop']}\n\n"
        "📌 Отправь фото с подписью вида:\n"
        "Ник: Vlad_Mensem\nРанг: 5\nДок-ва: Скриншот пополнения фам счёта"
    )

@dp.message(F.photo)
async def handle_shop_request(message: types.Message):
    if message.chat.type != "private":
        return
    if not message.caption:
        return await message.answer("❌ Нужно отправить фото с подписью!")

    if data["idea_chat"] is None:
        return await message.answer("❌ Чат идей не настроен!")

    # клавиатура
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Выдано", callback_data=f"approve:{message.from_user.id}")
    kb.button(text="❌ Отказано", callback_data=f"deny:{message.from_user.id}")
    kb.adjust(2)

    # пересылаем заявку в чат идей
    await bot.send_photo(
        chat_id=data["idea_chat"],
        photo=message.photo[-1].file_id,
        caption=f"🛒 Заявка из /shop:\n\n{message.caption}\n\n👤 От: {message.from_user.mention_html()}",
        reply_markup=kb.as_markup()
    )
    await message.answer("✅ Заявка отправлена администрации.")

# --- ОБРАБОТКА КНОПОК ---
@dp.callback_query(F.data.startswith("approve"))
async def cb_approve(call: types.CallbackQuery):
    uid = int(call.data.split(":")[1])
    await bot.send_message(uid, "✅ Твоя заявка одобрена!")
    await call.answer("Одобрено ✔")

@dp.callback_query(F.data.startswith("deny"))
async def cb_deny(call: types.CallbackQuery):
    uid = int(call.data.split(":")[1])
    await bot.send_message(uid, "❌ Твоя заявка отклонена.")
    await call.answer("Отклонено ✖")

# --- STAFF ---
@dp.message(Command("staff"))
async def cmd_staff(message: types.Message):
    staff_list = []
    for uid in data["admins"]:
        try:
            user = await bot.get_chat(uid)
            staff_list.append(user.first_name if not user.username else f"@{user.username}")
        except:
            staff_list.append(str(uid))
    staff_str = ", ".join(staff_list) if staff_list else "нет"
    await message.answer(
        f"👑 Создатель: <code>{CREATOR_ID}</code>\n"
        f"🛡 Админы: {staff_str}"
    )

# --- ДОБАВЛЕНИЕ/УДАЛЕНИЕ АДМИНА ЧЕРЕЗ РЕПЛАЙ ---
@dp.message(Command("addadmin"))
async def cmd_addadmin(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Только создатель может добавлять админов.")
    if message.reply_to_message:
        uid = message.reply_to_message.from_user.id
        data["admins"].add(uid)
        return await message.answer(f"✅ {message.reply_to_message.from_user.mention_html()} теперь админ.")
    await message.answer("❌ Ответь командой /addadmin на сообщение пользователя.")

@dp.message(Command("unadmin"))
async def cmd_unadmin(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Только создатель может удалять админов.")
    if message.reply_to_message:
        uid = message.reply_to_message.from_user.id
        if uid in data["admins"]:
            data["admins"].remove(uid)
            return await message.answer(f"✅ {message.reply_to_message.from_user.mention_html()} больше не админ.")
        else:
            return await message.answer("❌ Этот пользователь не админ.")
    await message.answer("❌ Ответь командой /unadmin на сообщение пользователя.")

# --- ИДЕИ ---
@dp.message(Command("idea"))
async def cmd_idea(message: types.Message):
    text = message.text.split(" ", 1)
    if len(text) > 1:
        if data["idea_chat"] is None:
            return await message.answer("❌ Чат идей не настроен!")
        await bot.send_message(data["idea_chat"], f"💡 Идея: {text[1]}\n👤 От {message.from_user.mention_html()}")
        await message.answer("✅ Идея отправлена администрации.")
    else:
        await message.answer("❌ Использование: /idea <ваша идея>", parse_mode=None)

# --- BOTSTATS ---
@dp.message(Command("botstats"))
async def cmd_botstats(message: types.Message):
    if not isCreator(message.from_user.id):
        return await message.answer("❌ Доступно только создателю.")
    await message.answer("📊 Статистика бота:\nПока пусто 🙂")

# --- HELP ---
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(data["help"], parse_mode=None)

# ======= ЗАПУСК =======
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
