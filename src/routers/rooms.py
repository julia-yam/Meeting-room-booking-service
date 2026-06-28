from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Room, User
from src.models.database import get_async_session
from src.routers.dependencies import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])

class RoomCreateSchema(BaseModel):
    name: str
    description: str | None = None

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreateSchema,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Room).where(Room.name == room_data.name)
    result = await db.execute(query)
    existing_room = result.scalar_one_or_none()
    
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Комната с таким названием уже существует"
        )
    
    new_room = Room(
        name=room_data.name,
        description=room_data.description
    )
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)
    
    return new_room


@router.get("/")
async def get_rooms(db: AsyncSession = Depends(get_async_session)):
    query = select(Room)
    result = await db.execute(query)
    rooms = result.scalars().all()
    return rooms