from decimal import Decimal
from locale import currency

from models import FlightPricesModel, PassengerModel, CostModel


class TicketCost:
    MAX_FREE_BAGGAGE_WEIGHT = 20

    def __init__(self, flight_prices: FlightPricesModel):
        self.flight_prices = flight_prices
        self._current_cost = Decimal(0)
    
    def add_passenger(self, passenger: PassengerModel):
        self._current_cost += self._ticket_cost(passenger)
        self._current_cost += self._baggage_cost(passenger)
        self._current_cost += self._pets_cost(passenger)

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
        return (passenger.baggage_weight - self.MAX_FREE_BAGGAGE_WEIGHT) * self.flight_prices.baggage_price

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
