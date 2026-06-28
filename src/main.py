from fastapi import FastAPI
from src.routers.auth import router as auth_router
from src.routers.rooms import router as rooms_router  # Добавили импорт

app = FastAPI(
    title="Booking API",
    description="API для бронирования переговорных комнат",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(rooms_router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API системы бронирования переговорных комнат"}