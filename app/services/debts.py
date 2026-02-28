from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Debt, DebtStatus


async def get_due_debts(session: AsyncSession, day: date) -> list[Debt]:
    stmt = (
        select(Debt)
        .where(Debt.due_date == day)
        .where(Debt.status == DebtStatus.ACTIVE)
    )
    return list((await session.scalars(stmt)).all())


def build_debt_reminder_text(debt: Debt) -> str:
    return (
        f"Búgin {debt.client_name}-nan {debt.amount} alıw kerek. "
        f"Tawar: {debt.item}. Telefon qılıń!"
    )
