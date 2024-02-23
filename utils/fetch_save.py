from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from datetime import datetime
from fastapi import HTTPException
import httpx
from db.models import ExchangeRate, CurrencyRate
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_rates(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Failed to fetch rates")
        return response.json()


async def save_rates(data: dict, session: AsyncSession) -> None:
    async with session.begin():
        stmt = select(ExchangeRate).where(ExchangeRate.base == data["base"])
        try:
            existing_rate = (await session.execute(stmt)).scalar_one()
            existing_rate.name = data["base"]
            existing_rate.updated_datetime = datetime.utcnow()
        except NoResultFound:
            exchange_rate = ExchangeRate(
                name=data["base"],
                base=data["base"],
                created_datetime=datetime.utcnow(),
                updated_datetime=datetime.utcnow()
            )
            session.add(exchange_rate)
            await session.flush()
            rate_id = exchange_rate.id
        else:
            rate_id = existing_rate.id

        for code, rate in data["rates"].items():
            stmt = select(CurrencyRate).where(
                CurrencyRate.exchange_rate_id == rate_id,
                CurrencyRate.currency_code == code)
            try:
                existing_currency_rate = (await session.execute(
                    stmt)).scalar_one()
                existing_currency_rate.rate = rate
            except NoResultFound:
                currency_rate = CurrencyRate(currency_code=code,
                                             rate=rate,
                                             exchange_rate_id=rate_id)
                session.add(currency_rate)
