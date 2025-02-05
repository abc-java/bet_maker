from pydantic import BaseModel, ConfigDict
from app.api.event.enum import EventState
import decimal


class BaseEvent(BaseModel):
    coefficient: decimal.Decimal
    deadline: int
    state: EventState


class Event(BaseEvent):
    id: int
    model_config = ConfigDict(from_attributes=True)
