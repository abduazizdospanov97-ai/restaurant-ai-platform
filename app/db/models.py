from __future__ import annotations

import enum
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy models."""


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class LanguageEnum(str, enum.Enum):
    QR = "QR"
    UZ = "UZ"
    RU = "RU"


class ProfessionEnum(str, enum.Enum):
    TAXI = "taxi"
    OTHER = "other"


class ExpenseCategoryEnum(str, enum.Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    HOUSEHOLD = "Household"
    INTERNET_PHONE = "Internet/Phone"
    CLOTHES = "Clothes"
    HEALTH = "Health"
    CHILDREN = "Children"
    ENTERTAINMENT = "Entertainment"
    TOY_MARESIM = "Toy-Maresim"
    DEBT = "Debt"


class ExpenseTypeEnum(str, enum.Enum):
    EXPENSE = "expense"
    DEBT_GIVEN = "debt_given"
    DEBT_REPAID_TO_ME = "debt_repaid_to_me"


class DebtDirectionEnum(str, enum.Enum):
    THEY_OWE_ME = "they_owe_me"
    I_OWE_THEM = "i_owe_them"


class DebtStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    PARTIAL = "partial"
    CLOSED = "closed"


class GoalStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Family(Base, TimestampMixin):
    __tablename__ = "families"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    family_code: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    owner_user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    spouse_user_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="owned_family",
        foreign_keys=[owner_user_id],
    )
    spouse: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="joined_family",
        foreign_keys=[spouse_user_id],
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    language: Mapped[LanguageEnum] = mapped_column(
        Enum(LanguageEnum, name="language_enum"),
        nullable=False,
        default=LanguageEnum.UZ,
    )
    profession: Mapped[ProfessionEnum] = mapped_column(
        Enum(ProfessionEnum, name="profession_enum"),
        nullable=False,
        default=ProfessionEnum.OTHER,
    )
    monthly_income: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="UZS")

    taxi_has_own_car: Mapped[Optional[bool]] = mapped_column(Boolean)
    taxi_daily_fuel_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))

    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    expenses: Mapped[list["Expense"]] = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    incomes: Mapped[list["Income"]] = relationship(
        "Income",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    debts: Mapped[list["Debt"]] = relationship(
        "Debt",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    goals: Mapped[list["Goal"]] = relationship(
        "Goal",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    owned_family: Mapped[Optional["Family"]] = relationship(
        "Family",
        back_populates="owner",
        foreign_keys="Family.owner_user_id",
        uselist=False,
    )
    joined_family: Mapped[Optional["Family"]] = relationship(
        "Family",
        back_populates="spouse",
        foreign_keys="Family.spouse_user_id",
        uselist=False,
    )


class Expense(Base, TimestampMixin):
    __tablename__ = "expenses"
    __table_args__ = (Index("ix_expenses_user_date", "user_id", "expense_date"),)

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="UZS")
    category: Mapped[ExpenseCategoryEnum] = mapped_column(
        Enum(ExpenseCategoryEnum, name="expense_category_enum"),
        nullable=False,
    )
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[ExpenseTypeEnum] = mapped_column(
        Enum(ExpenseTypeEnum, name="expense_type_enum"),
        nullable=False,
        default=ExpenseTypeEnum.EXPENSE,
    )
    expense_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    user: Mapped["User"] = relationship("User", back_populates="expenses")


class Income(Base, TimestampMixin):
    __tablename__ = "incomes"
    __table_args__ = (Index("ix_incomes_user_date", "user_id", "income_date"),)

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="UZS")
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    income_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    user: Mapped["User"] = relationship("User", back_populates="incomes")


class Debt(Base, TimestampMixin):
    __tablename__ = "debts"
    __table_args__ = (
        Index("ix_debts_user_direction_status", "user_id", "direction", "status"),
        UniqueConstraint("user_id", "person_name", "created_at", name="uq_debt_person_entry"),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    person_name: Mapped[str] = mapped_column(String(255), nullable=False)
    direction: Mapped[DebtDirectionEnum] = mapped_column(
        Enum(DebtDirectionEnum, name="debt_direction_enum"),
        nullable=False,
    )
    principal_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    remaining_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="UZS")
    status: Mapped[DebtStatusEnum] = mapped_column(
        Enum(DebtStatusEnum, name="debt_status_enum"),
        nullable=False,
        default=DebtStatusEnum.ACTIVE,
    )
    issued_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    note: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["User"] = relationship("User", back_populates="debts")


class Goal(Base, TimestampMixin):
    __tablename__ = "goals"
    __table_args__ = (Index("ix_goals_user_status", "user_id", "status"),)

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    target_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    current_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="UZS")
    deadline: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[GoalStatusEnum] = mapped_column(
        Enum(GoalStatusEnum, name="goal_status_enum"),
        nullable=False,
        default=GoalStatusEnum.ACTIVE,
    )

    user: Mapped["User"] = relationship("User", back_populates="goals")
