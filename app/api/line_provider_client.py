from app.settings import settings
from app.api.event.schema import Event
from app.api.event.enum import EventState
from fastapi_pagination import Page
import aiohttp


async def get_event(event_id: int) -> Event | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.LINE_PROVIDER_URL}/api/events/{event_id}"
        ) as resp:
            if resp.status == 200:
                return Event(**(await resp.json()))
            else:
                return None


async def get_actual_events(page: int, size: int) -> Page[Event]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.LINE_PROVIDER_URL}/api/events/",
            params={"state_filter": EventState.NEW, "page": page, "size": size},
        ) as resp:
            return await resp.json()
