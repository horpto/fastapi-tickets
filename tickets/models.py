import datetime
from decimal import Decimal

from enum import Enum
from pydantic import BaseModel, Field, PositiveInt

from storage import Storage

class PassengerModel(BaseModel):
    age: PositiveInt
    baggage_weight: PositiveInt | None = None
    pets_num: PositiveInt | None = None


class Cities(str, Enum):
    kaliningrad = "Калининград"
    moscow = "Москва"
    petersburg = "Санкт-Петербург"


class Currency(str, Enum):
    rub = 'RUB'


class FlightModel(BaseModel):
    src: Cities
    dst: Cities
    time: datetime.time


class FlightPricesModel(FlightModel):
    adult_cost: Decimal
    teenager_cost: Decimal
    child_cost: Decimal
    baggage_price: Decimal
    pet_price: Decimal
    seats_num: PositiveInt
    currency: Currency
    storage = Field('file', exclude=True)

    @classmethod
    async def from_storage(cls, storage: Storage, flight: FlightModel):
        key = f'flight_{flight.src}_{flight.dst}_{flight.time}'
        value = await storage.get_by_key(key)
        return cls(storage=storage, **value)

    async def save(self):
        key = f'flight_{self.src}_{self.dst}_{self.time}'
        value = self.dict()
        await self.storage.set_by_key(key, value)


class CostModel(BaseModel):
    cost: Decimal
    cost_currency: Currency

