from fastapi import APIRouter, Depends, Query
from app.api.event import schema
from app.db import get_session, AsyncSession
from fastapi_pagination import Page
from typing import Annotated
from app.api.line_provider_client import get_actual_events

router = APIRouter(prefix="/events")


@router.get("/", response_model=Page[schema.Event])
async def read_all(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 50,
    session: AsyncSession = Depends(get_session),
) -> Page[schema.Event]:
    return await get_actual_events(page, size)
