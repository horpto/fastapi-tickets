from decimal import Decimal
from locale import currency
from math import ceil

from numpy import full

from models import CostModel, FlightPricesModel, PassengerModel


class TicketCostCalculator:
    MAX_FREE_BAGGAGE_WEIGHT = 20

    def __init__(self, flight_prices: FlightPricesModel):
        self.flight_prices = flight_prices
        self._current_cost = Decimal(0)

    def add_passenger(self, passenger: PassengerModel):
        full_cost = self._ticket_cost(passenger)
        full_cost += self._baggage_cost(passenger)
        full_cost += self._pets_cost(passenger)

        self._current_cost += full_cost

    def _ticket_cost(self, passenger: PassengerModel):
        if passenger.age >= 18:
            return self.flight_prices.adult_cost
        if passenger.age > 5:
            return self.flight_prices.teenager_cost
        return self.flight_prices.child_cost

    def _baggage_cost(self, passenger: PassengerModel):
        if not passenger.baggage_weight:
            return 0
        if passenger.baggage_weight <= self.MAX_FREE_BAGGAGE_WEIGHT:
            return 0
        weight_diff = passenger.baggage_weight - self.MAX_FREE_BAGGAGE_WEIGHT
        min_weight = self.flight_prices.baggage_weight
        return ceil(weight_diff / min_weight) * self.flight_prices.baggage_price

    def _pets_cost(self, passenger: PassengerModel):
        if passenger.pets_num:
            return passenger.pets_num * self.flight_prices.pet_price
        return 0

    @property
    def current_cost(self):
        return CostModel(
            cost=self._current_cost,
            currency=self.flight_prices.currency,
        )
