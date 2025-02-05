from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from app.api.bet.enum import BetState


class BaseBet(BaseModel):
    event_id: int
    amount: Decimal = Field(ge=0.01, decimal_places=2)
    state: BetState


class Bet(BaseBet):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CreateBetResponse(Bet):
    pass


class CreateBetRequest(BaseBet):
    pass


class UpdateBetResponse(Bet):
    pass


class UpdateBetRequest(BaseModel):
    event_id: int | None = None
    amount: Decimal | None = Field(ge=0.01, decimal_places=2, default=None)
    state: BetState | None = None
