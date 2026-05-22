from datetime import date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Transaction, TransactionType


async def _income_sum_by_day(session: AsyncSession, user_id: int, day: date) -> int:
    start = datetime.combine(day, datetime.min.time())
    end = start + timedelta(days=1)
    stmt = (
        select(func.coalesce(func.sum(Transaction.amount), 0))
        .where(Transaction.user_id == user_id)
        .where(Transaction.type == TransactionType.INCOME)
        .where(Transaction.created_at >= start)
        .where(Transaction.created_at < end)
    )
    return int((await session.execute(stmt)).scalar_one())


async def build_income_comparison_text(session: AsyncSession, user_id: int) -> str:
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    today_income = await _income_sum_by_day(session, user_id, today)
    yesterday_income = await _income_sum_by_day(session, user_id, yesterday)

    if today_income > yesterday_income:
        mood = "Zor! Búgin sawda kóp."
    elif today_income < yesterday_income:
        mood = "Búgin sawda azıraq."
    else:
        mood = "Búgin menen keshe birdey sawda boldı."

    return (
        f"Búgin: {today_income}\n"
        f"Keshe: {yesterday_income}\n"
        f"{mood}"
    )
