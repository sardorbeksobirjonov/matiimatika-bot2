import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram import F
import asyncio

# 🤖 Bot tokenni shu yerga yozing
TOKEN = "7444816748:AAH_hIt_S-p_lFrsNYy5JJkkpw7mJGmW4po"

# 🔐 Admin maxsus kod
ADMIN_CODE = "admin123"

# 📋 Logger sozlash
logging.basicConfig(level=logging.INFO)

# 📦 Saqlovchi
storage = MemoryStorage()

# 🤖 Bot va Dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

# 🧑‍💻 O‘yinchilarni saqlovchi dict
players = {}

# 🎮 /start komandasi
@dp.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user
    players[user.id] = {
        "step": "ask_count",
        "score": 0,
        "total": 0,
        "questions_left": 0,
        "current_question": "",
        "name": user.full_name,
        "username": user.username or f"id{user.id}"
    }

    await message.answer(
        f"👋 <b>Assalomu alaykum, {user.full_name}! 👾</b>\n\n"
        "Men — 🤖 <b>Qidaar</b>, sizning aqlli matematik do‘stingiz! 🧠✨\n\n"
        "🎯 <i>O‘yin boshlanishi uchun tayyor bo‘ling!</i>\n"
        "🧮 Sizga qiziqarli va hayajonli savollar beraman.\n\n"
        "✅ <b>To‘g‘ri javob:</b> +5 ball 🎉\n"
        "❌ <b>Noto‘g‘ri javob:</b> -2 ball 😢\n\n"
        "🔢 Endi esa, nechta savol yechishni xohlaysiz? (Masalan: 5)\n\n"
        "📩 Javobingizni yozing va o‘yinni boshlaymiz!\n\n"
        "https://t.me/webstormers"
    )

# 📩 Barcha xabarlarga ishlovchi handler
@dp.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    # 🛡 ADMIN KODI
    if text == ADMIN_CODE:
        if not players:
            await message.answer("📭 Hech qanday o‘yinchi topilmadi.")
            return

        response = "👑 <b>Barcha ishtirokchilar natijasi:</b>\n\n"
        for p_id, p in players.items():
            mention = f"<a href='tg://user?id={p_id}'>@{p['username']}</a>"
            response += f"🧑 {mention} — <b>{p['score']} ball</b>\n"
        await message.answer(response)
        return

    # 🔐 Ro‘yxatdan o‘tmagan foydalanuvchi
    if user_id not in players:
        await message.answer("🔰 Iltimos, avval /start buyrug‘ini yuboring.")
        return

    player = players[user_id]

    # 🔢 Savollar sonini kiritish bosqichi
    if player["step"] == "ask_count":
        if not text.isdigit():
            await message.answer("⚠️ Son kiriting. Masalan: 5")
            return
        count = int(text)
        player["total"] = count
        player["questions_left"] = count
        player["step"] = "playing"
        await send_question(message, player)
        return

    # ❓ Savollarga javob bosqichi
    elif player["step"] == "playing":
        try:
            user_answer = int(text)
        except ValueError:
            await message.answer("🔢 Iltimos, faqat son kiriting.")
            return

        correct = eval(player["current_question"])
        if user_answer == correct:
            player["score"] += 5
            await message.answer("✅ <b>To‘g‘ri javob!</b> +5 ball 💥")
        else:
            player["score"] -= 2
            await message.answer(f"❌ <b>Noto‘g‘ri.</b> To‘g‘ri javob: <b>{correct}</b> 😢 (-2 ball)")

        player["questions_left"] -= 1

        if player["questions_left"] > 0:
            await send_question(message, player)
        else:
            await message.answer(
                f"🏁 <b>O‘yin tugadi!</b>\n\n"
                f"🧮 Savollar soni: <b>{player['total']}</b>\n"
                f"🥇 Umumiy ball: <b>{player['score']}</b>\n"
                f"👏 Yaxshi harakat! Yana o‘ynash uchun /start ni bosing."
            )
            player["step"] = "done"

# 🧮 Savol yuboruvchi funksiya
async def send_question(message: Message, player: dict):
    a = random.randint(50, 70)
    b = random.randint(10, 30)
    c = random.randint(2, 12)
    question = f"{a} - {b} + {c}"
    player["current_question"] = question
    current = player["total"] - player["questions_left"] + 1
    await message.answer(f"🧠 <b>{current}-savol:</b>\n\n🔢 {question} = ?")

# ▶️ Botni ishga tushurish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
