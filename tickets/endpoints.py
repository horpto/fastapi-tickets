from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_storage
from logic import TicketCost
from models import CostModel, FlightModel, FlightPricesModel, PassengerModel
from storage import Storage

router = APIRouter()


@router.post(
    "/passenger-cost",
    summary="цена полета пассажира",
    response_model=CostModel,
)
async def ticket_price(
    flight: FlightModel,
    passenger: PassengerModel = None,
    passengers: list[PassengerModel] = None,
    storage: Storage = Depends(get_storage),
):
    if not (passenger or passengers):
        raise HTTPException(status_code=400, detail="Specify any passenger")
    if passenger and passengers:
        raise HTTPException(status_code=400, detail="Specify only one of field: passenger, passengers")
    if passenger:
        passengers = [passenger]

    flight_prices: FlightPricesModel = await FlightPricesModel.from_storage(storage, flight)

    ticket_cost = TicketCost(flight_prices)
    for passenger in passengers:
        ticket_cost.add_passenger(passenger)
    return ticket_cost.current_cost
