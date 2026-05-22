import json
from datetime import datetime, timezone

from openai import AsyncOpenAI

from app.config import get_settings
from app.schemas import CategorizationResult, DebtParseResult

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)

CATEGORY_SYSTEM_PROMPT = """
Sen "Qaltasha" botısan. Paydalanıwshı kirim yamasa shıǵım jazadı.
Sen onı analizlep, tómendegi kategoriyalardan birine qos:
[Aziq-awqat, Komunal, Transport, Shaqiriq/Toy, Kiyim, Dori-darmon, Basqa].

Juwaptı tek JSON formatında qaytar:
{"category": "...", "amount": ..., "type": "expense/income", "comment": "..."}
""".strip()

DEBT_SYSTEM_PROMPT_TEMPLATE = """
Paydalanıwshı nasiya (qarız) maǵlıwmatın kirgizbekte.
Tekstten mına maǵlıwmatlardı ajıratıp al:
1. Klient atı (Name)
2. Tovar (Item)
3. Summa (Amount)
4. Qaytarıw sánesi (Due Date) - format YYYY-MM-DD.

Eger tekstte salıstırmalı waqıt bolsa (mısal: "erteń", "10 kúnnen keyin"), buginiń sánesinen esapla.
Búgingi sáne: {today}

Juwaptı tek JSON formatında qaytar.
""".strip()


async def _json_completion(system_prompt: str, user_text: str) -> dict:
    response = await client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        response_format={"type": "json_object"},
    )
    content = response.output_text
    return json.loads(content)


async def categorize_transaction(user_text: str) -> CategorizationResult:
    data = await _json_completion(CATEGORY_SYSTEM_PROMPT, user_text)
    return CategorizationResult.model_validate(data)


async def parse_debt_entry(user_text: str) -> DebtParseResult:
    today = datetime.now(timezone.utc).date().isoformat()
    prompt = DEBT_SYSTEM_PROMPT_TEMPLATE.format(today=today)
    data = await _json_completion(prompt, user_text)
    return DebtParseResult.model_validate(data)
