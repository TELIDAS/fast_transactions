import os
from fastapi import APIRouter

from db.schemas import (
    LatestExchangeRateResponse,
    CurrencyConversionResponse,
    ExchangeRateModel,
    SuccessResponse
)
from utils.fetch_save import fetch_rates, save_rates

from fastapi import HTTPException, Depends

from db.models import ExchangeRate
from sqlalchemy import select
from utils.converter import get_rate
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import SessionLocal

app = FastAPI()

router = APIRouter()


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.post("/save-or-update-rates/",
             response_model=SuccessResponse)
async def fetch_and_store_rates(
        session: AsyncSession = Depends(get_session)):
    api_key = os.getenv("API_KEY")
    url = f'http://api.exchangeratesapi.io/v1/latest?access_key={api_key}'
    data = await fetch_rates(url)
    await save_rates(data, session)
    return {"success": "Data added successfully"}


@router.get("/convert/",
            response_model=CurrencyConversionResponse)
async def convert_endpoint(
        from_currency: str,
        to_currency: str,
        amount: float,
        session: AsyncSession = Depends(get_session)
):
    rate = await get_rate(from_currency, to_currency, session)
    converted_amount = amount * rate
    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "original_amount": amount,
        "converted_amount": converted_amount
    }


@router.get("/latest-exchange-rate/",
            response_model=LatestExchangeRateResponse)
async def get_latest_rate(
        session: AsyncSession = Depends(get_session)):
    async with session.begin():
        stmt = select(ExchangeRate).order_by(
            ExchangeRate.updated_datetime.desc()).limit(1)
        result = await session.execute(stmt)
        latest_exchange_rate = result.scalars().first()

        if not latest_exchange_rate:
            raise HTTPException(status_code=404,
                                detail="No exchange rates found")

        return {
            "created_datetime":
                latest_exchange_rate.created_datetime,
            "updated_datetime":
                latest_exchange_rate.updated_datetime
        }
