from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import ExchangeRate, CurrencyRate


async def get_rate(from_currency: str,
                   to_currency: str,
                   session: AsyncSession) -> float:
    from_rate_stmt = (
        select(CurrencyRate.rate)
        .join(ExchangeRate, ExchangeRate.id == CurrencyRate.exchange_rate_id)
        .where(CurrencyRate.currency_code == from_currency,
               ExchangeRate.base == 'EUR')
    )
    to_rate_stmt = (
        select(CurrencyRate.rate)
        .join(ExchangeRate, ExchangeRate.id == CurrencyRate.exchange_rate_id)
        .where(CurrencyRate.currency_code == to_currency,
               ExchangeRate.base == 'EUR')
        # In Free plan there is only one base
    )

    from_rate_result = await session.execute(from_rate_stmt)
    from_rate = from_rate_result.scalars().first()

    to_rate_result = await session.execute(to_rate_stmt)
    to_rate = to_rate_result.scalars().first()

    if from_rate and to_rate:
        return (1 / from_rate) * to_rate

    raise HTTPException(
        status_code=404,
        detail="Exchange rate not found for one or both currencies")
