from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class ExchangeRate(Base):
    __tablename__ = 'exchange_rates'

    id = Column(Integer,
                primary_key=True,
                index=True)
    name = Column(String)
    base = Column(String)
    created_datetime = Column(DateTime,
                              default=func.now())
    updated_datetime = Column(DateTime,
                              default=func.now(),
                              onupdate=func.now())
    rates = relationship("CurrencyRate",
                         back_populates="exchange_rate")


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True, index=True)
    currency_code = Column(String, index=True)
    rate = Column(Float)
    exchange_rate_id = Column(Integer, ForeignKey('exchange_rates.id'))
    exchange_rate = relationship("ExchangeRate", back_populates="rates")
