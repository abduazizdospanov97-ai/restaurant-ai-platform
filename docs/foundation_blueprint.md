# Qaltasha AI Foundation Blueprint

## 1) Proposed Folder Structure

```text
restaurant-ai-platform/
├── app/
│   ├── bot/
│   │   ├── handlers/
│   │   │   ├── start.py
│   │   │   ├── expenses.py
│   │   │   ├── analytics.py
│   │   │   ├── debts.py
│   │   │   ├── family.py
│   │   │   └── goals.py
│   │   ├── keyboards/
│   │   │   ├── common.py
│   │   │   └── analytics.py
│   │   ├── middlewares/
│   │   │   └── user_context.py
│   │   └── states/
│   │       └── onboarding.py
│   ├── core/
│   │   ├── config.py
│   │   ├── prompts.py
│   │   └── logging.py
│   ├── db/
│   │   ├── models.py
│   │   ├── session.py
│   │   ├── base.py
│   │   └── repositories/
│   │       ├── users.py
│   │       ├── expenses.py
│   │       ├── incomes.py
│   │       ├── debts.py
│   │       ├── families.py
│   │       └── goals.py
│   ├── services/
│   │   ├── nlp_parser.py
│   │   ├── advisor.py
│   │   ├── red_zone.py
│   │   ├── analytics.py
│   │   └── excel_export.py
│   ├── utils/
│   │   ├── currency.py
│   │   ├── locale.py
│   │   └── datetime.py
│   └── main.py
├── alembic/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   └── foundation_blueprint.md
├── requirements.txt
└── .env.example
```

## 2) Claude Haiku NLP Parser Prompt

Implemented in `app/core/prompts.py` as `HAIKU_EXPENSE_PARSER_SYSTEM_PROMPT`.

Usage pattern (as requested):

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_KEY")
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{"role": "user", "content": user_text}]
)
result = message.content[0].text
```

Recommended parser call contract:
- Pass system prompt from `HAIKU_EXPENSE_PARSER_SYSTEM_PROMPT`.
- Pass raw user text in `user` message.
- Validate JSON response with Pydantic before writing to DB.

## 3) SQLAlchemy Async Data Foundation

Implemented in `app/db/models.py`:
- `User`
- `Expense`
- `Income`
- `Debt`
- `Family`
- `Goal`

Design notes:
- UUID primary keys for safe multi-service growth.
- Explicit enums for language, category, debt direction/status, goal status.
- Indexed date columns for period analytics (today/week/month).
- Taxi onboarding fields included directly in `User`:
  - `taxi_has_own_car`
  - `taxi_daily_fuel_cost`
- `Family` has unique `family_code` for spouse linking.

## 4) Step-by-Step Build Plan (Module by Module)

1. **Project Bootstrap**
   - Add dependencies: `aiogram`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `anthropic`, `pandas`, `matplotlib`, `openpyxl`, `pydantic-settings`.
   - Configure `.env` + typed settings.

2. **Database Layer**
   - Implement `db/session.py` with `create_async_engine` + `async_sessionmaker`.
   - Add Alembic config and generate first migration from `models.py`.
   - Create repository classes for each aggregate.

3. **Bot Skeleton (aiogram 3.x)**
   - Initialize dispatcher/router tree.
   - Register global middleware for loading user locale/profile.
   - Add shared reply keyboards.

4. **Onboarding Module**
   - `/start` FSM: language → profession → monthly income.
   - Taxi branch: own/rented car + daily fuel cost.
   - Persist in `users` table and mark onboarding complete.

5. **NLP Input Engine (Claude Haiku)**
   - `services/nlp_parser.py` with strict JSON extraction pipeline:
     1) call Claude Haiku,
     2) parse JSON,
     3) validate schema,
     4) map to domain commands.
   - Add typo and language robustness tests.

6. **Expense & Debt Command Handling**
   - Convert parsed payloads into `Expense` and/or `Debt` records.
   - Implement debt flows: who owes me / who I owe.

7. **Red Zone Logic**
   - Add `red_zone.py`: if category is `Toy-Maresim` and amount > 20% monthly income, trigger warning text in user language.

8. **Analytics Module**
   - Period aggregations: today/week/month.
   - Matplotlib pie chart generation by category.
   - Pandas Excel export (`.xlsx`) for selected period.

9. **Family Module**
   - Generate unique `family_code`.
   - Link spouse account by code.
   - Add family-level analytics rollups.

10. **Goals Module**
   - CRUD for savings goals.
   - Progress tracking from manual top-ups and optional surplus logic.

11. **AI Financial Advisor (Claude Sonnet)**
   - Monthly summary generator from aggregated DB stats.
   - Send summary to `claude-sonnet-4-6` for personalized recommendations in QR/UZ/RU.

12. **Quality & Production Readiness**
   - Unit tests for parsers/repositories.
   - Integration tests for onboarding + expense pipeline.
   - Structured logs, retry policy for Anthropic, and idempotency guards for Telegram updates.
