from app.db import AsyncSession
from app.models import Bet
from app.api.bet import schema
from app.api.bet.enum import BetState
from typing import AsyncIterator
from app.api import line_provider_client
from fastapi import HTTPException
import decimal


async def get_bets(session: AsyncSession) -> AsyncIterator[schema.Bet]:
    async with session() as session:
        async for event in Bet.read_all(session):
            yield schema.Bet.model_validate(event)


async def create_bet(
    session: AsyncSession, amount: decimal.Decimal, event_id: int, state: BetState
) -> schema.Bet:
    async with session.begin() as session:
        response = await line_provider_client.get_event(event_id)
        if not response:
            raise HTTPException(status_code=404)

        bet = await Bet.create(session, amount, event_id, state)
        return schema.Bet.model_validate(bet)


async def update_bet(
    session: AsyncSession,
    id: int,
    amount: decimal.Decimal = None,
    event_id: int = None,
    state: BetState = None,
) -> schema.Bet:
    async with session.begin() as session:
        bet = await Bet.read_by_id(session, id)
        if not bet:
            raise HTTPException(status_code=404)

        await bet.update(session, amount=amount, event_id=event_id, state=state)
        await session.refresh(bet)
        return schema.Bet.model_validate(bet)


async def update_bet_state_from_event(
    session: AsyncSession, event_id: int, state: BetState
) -> AsyncIterator[schema.Bet]:
    async with session.begin() as session:
        for bet in await Bet.find_bets_on_event(session, event_id):
            await bet.update(session, state=state)
            await session.refresh(bet)
            yield schema.Bet.model_validate(bet)
