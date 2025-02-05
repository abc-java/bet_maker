from __future__ import annotations

from typing import AsyncIterator
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from typing_extensions import Annotated
from app.api.bet.enum import BetState
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


class Bet(Base):
    __tablename__ = "bet"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Annotated[Decimal, 2]]
    event_id: Mapped[int]
    state: Mapped[BetState]

    @classmethod
    async def read_by_id(cls, session: AsyncSession, bet_id: int) -> Bet | None:
        stmt = select(cls).where(cls.id == bet_id)
        return await session.scalar(stmt)

    @classmethod
    async def find_bets_on_event(
        cls, session: AsyncSession, event_id: int
    ) -> AsyncIterator[Bet]:
        stmt = select(cls).where(cls.event_id == event_id)
        bets = await session.scalars(stmt)
        return bets

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[Bet]:
        stmt = select(cls)

        stream = await session.stream_scalars(stmt)
        async for row in stream:
            yield row

    @classmethod
    async def create(
        cls, session: AsyncSession, amount: Decimal, event_id: int, state: BetState
    ) -> Bet:
        bet = Bet(amount=amount, event_id=event_id, state=state)
        session.add(bet)
        await session.flush()
        return bet

    async def update(self, session: AsyncSession, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)
        await session.flush()
