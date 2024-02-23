from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class ExchangeRateBase(BaseModel):
    name: Optional[str] = None
    base: str
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "Default Rate",
                    "base": "USD",
                }
            ]
        }


class ExchangeRateCreate(ExchangeRateBase):
    pass


class ExchangeRateModel(ExchangeRateBase):
    id: int
    rates: List['CurrencyRateModel'] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "name": "Default Rate",
                    "base": "USD",
                    "created_datetime": "2024-02-23T21:09:52.457569",
                    "updated_datetime": "2024-02-23T21:10:04.793889",
                    "rates": [
                        {"id": 1, "currency_code": "USD", "rate": 1.0, "exchange_rate_id": 1},
                        {"id": 2, "currency_code": "EUR", "rate": 0.9, "exchange_rate_id": 1}
                    ]
                }
            ]
        }


class CurrencyRateModel(BaseModel):
    id: int
    currency_code: str
    rate: float
    exchange_rate_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "currency_code": "USD",
                    "rate": 1.0,
                    "exchange_rate_id": 1,
                },
                {
                    "id": 2,
                    "currency_code": "EUR",
                    "rate": 0.9,
                    "exchange_rate_id": 1,
                }
            ]
        }


class CurrencyConversionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "from_currency": "USD",
                    "to_currency": "EUR",
                    "amount": 100,
                }
            ]
        }


class CurrencyConversionResponse(BaseModel):
    from_currency: str
    to_currency: str
    original_amount: float
    converted_amount: float

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "from_currency": "USD",
                    "to_currency": "EUR",
                    "original_amount": 100,
                    "converted_amount": 90,
                }
            ]
        }


class LatestExchangeRateResponse(BaseModel):
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "created_datetime": "2024-02-23T21:09:52.457569",
                    "updated_datetime": "2024-02-23T21:10:04.793889",
                }
            ]
        }


class SuccessResponse(BaseModel):
    success: str
