from fastapi import APIRouter, Depends
from app.api.bet import service, schema
from app.db import get_session, AsyncSession
from fastapi_pagination import Page, paginate
from app.api.bet.enum import BetState


router = APIRouter(prefix="/bets")


@router.get("/", response_model=Page[schema.Bet])
async def read_all(session: AsyncSession = Depends(get_session)) -> Page[schema.Bet]:
    return paginate([bet async for bet in service.get_bets(session)])


@router.post("/", response_model=schema.CreateBetResponse)
async def create(
    data: schema.CreateBetRequest, session: AsyncSession = Depends(get_session)
) -> schema.Bet:
    return await service.create_bet(session, data.amount, data.event_id, data.state)


@router.put("/{id}", response_model=schema.UpdateBetResponse)
async def update(
    id: int, data: schema.UpdateBetRequest, session: AsyncSession = Depends(get_session)
) -> schema.Bet:
    return await service.update_bet(session, id, data.amount, data.event_id, data.state)


@router.put(
    "/update-state-from-event/{event_id}", response_model=list[schema.Bet] | schema.Bet
)
async def update_from_event(
    event_id: int, state: BetState, session: AsyncSession = Depends(get_session)
) -> list[schema.Bet] | schema.Bet:
    return [
        bet
        async for bet in service.update_bet_state_from_event(session, event_id, state)
    ]
