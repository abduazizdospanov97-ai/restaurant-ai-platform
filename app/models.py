from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Role(str, Enum):
    XALIQ = "xaliq"
    DUKAN = "dukan"
    BREND = "brend"


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class DebtStatus(str, Enum):
    ACTIVE = "active"
    PAID = "paid"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[Role] = mapped_column(SQLEnum(Role), nullable=False)
    salary: Mapped[int | None] = mapped_column(Integer, nullable=True)
    limits: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    transactions: Mapped[list[Transaction]] = relationship(back_populates="user")
    debts: Mapped[list[Debt]] = relationship(back_populates="merchant")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="transactions")


class Debt(Base):
    __tablename__ = "debts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    merchant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    client_name: Mapped[str] = mapped_column(String(128), nullable=False)
    client_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    item: Mapped[str] = mapped_column(String(256), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[DebtStatus] = mapped_column(SQLEnum(DebtStatus), default=DebtStatus.ACTIVE, nullable=False)

    merchant: Mapped[User] = relationship(back_populates="debts")
