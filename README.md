# Restaurant AI Platform (MVP)

This repository contains a starter implementation for the **Development** stage of your Telegram finance/debt assistant.

## Stack
- **Bot**: `aiogram` v3
- **DB**: PostgreSQL via `SQLAlchemy` async engine
- **AI parsing**: `openai` responses API (JSON-only outputs)
- **Scheduling**: `APScheduler`
- **Secrets**: `python-dotenv` + environment variables

## Quick start
1. Create and activate a virtualenv.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables in `.env` (see `.env.example`).
4. Run migrations with your preferred tool (Alembic recommended; models are included).
5. Start the bot:
   ```bash
   python bot.py
   ```

## Implemented logic
- Expense/income AI categorization prompt with strict JSON schema.
- Debt parsing prompt with due-date extraction target format `YYYY-MM-DD`.
- Category spending limit checks for monthly spending.
- Daily debt reminder scheduler (09:00 UTC by default).
- Today vs yesterday income statistics summary.

## Next steps
- Add Alembic migration scripts.
- Add authentication/role setup flow for users.
- Add richer aiogram handlers and keyboards.
