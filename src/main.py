from fastapi import FastAPI
from src.routers.auth import router as auth_router
from src.routers.rooms import router as rooms_router 
from src.routers.bookings import router as bookings_router
from src.models.database import engine
from src.models.base import Base

app = FastAPI(
    title="Booking API",
    description="API для бронирования переговорных комнат",
    version="1.0.0"
)

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована")

app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(bookings_router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API системы бронирования переговорных комнат"}