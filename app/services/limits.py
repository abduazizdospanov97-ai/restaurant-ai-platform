from datetime import datetime

from sqlalchemy import Select, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Transaction, TransactionType, User


async def check_limit_before_expense(
    session: AsyncSession,
    user_id: int,
    category: str,
    new_amount: int,
) -> tuple[bool, int, int]:
    user = await session.get(User, user_id)
    if not user or not user.limits:
        return True, 0, 0

    limit_amount = int(user.limits.get(category, 0))
    if limit_amount <= 0:
        return True, 0, 0

    now = datetime.utcnow()
    stmt: Select = (
        select(func.coalesce(func.sum(Transaction.amount), 0))
        .where(Transaction.user_id == user_id)
        .where(Transaction.category == category)
        .where(Transaction.type == TransactionType.EXPENSE)
        .where(extract("year", Transaction.created_at) == now.year)
        .where(extract("month", Transaction.created_at) == now.month)
    )

    current_month_spent = int((await session.execute(stmt)).scalar_one())
    projected_total = current_month_spent + new_amount
    is_allowed = projected_total <= limit_amount
    remaining = max(limit_amount - projected_total, 0)
    return is_allowed, remaining, limit_amount
