from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app.api.bet.routers import router as bet_router
from app.api.event.routers import router as event_router


app = FastAPI()
add_pagination(app)

app.include_router(bet_router, prefix="/api")
app.include_router(event_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
