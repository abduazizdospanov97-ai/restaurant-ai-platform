import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import get_settings
from app.db import SessionLocal
from app.services.ai_parser import categorize_transaction
from app.services.debts import build_debt_reminder_text, get_due_debts
from app.services.stats import build_income_comparison_text

settings = get_settings()
bot = Bot(token=settings.bot_token)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Sálem! Kirim/shıǵım yaki qarız tekstin jaziń.\n"
        "Statistika ushın: /stats"
    )


@dp.message(F.text == "/stats")
async def stats(message: Message) -> None:
    async with SessionLocal() as session:
        text = await build_income_comparison_text(session, message.from_user.id)
    await message.answer(text)


@dp.message(F.text)
async def parse_text(message: Message) -> None:
    parsed = await categorize_transaction(message.text)
    await message.answer(
        "AI analizı:\n"
        f"- category: {parsed.category}\n"
        f"- amount: {parsed.amount}\n"
        f"- type: {parsed.type}\n"
        f"- comment: {parsed.comment}"
    )


async def send_due_debt_reminders() -> None:
    today = datetime.utcnow().date()
    async with SessionLocal() as session:
        debts = await get_due_debts(session, today)

    for debt in debts:
        await bot.send_message(chat_id=debt.merchant_id, text=build_debt_reminder_text(debt))


async def main() -> None:
    scheduler.add_job(send_due_debt_reminders, "cron", hour=settings.reminder_hour_utc)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
