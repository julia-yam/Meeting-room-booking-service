from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Room, User, Slot
from src.models.database import get_async_session
from src.routers.dependencies import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])

class RoomCreateSchema(BaseModel):
    name: str
    description: str | None = None

class SlotCreateSchema(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime

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

@router.post("/slots", status_code=status.HTTP_201_CREATED)
async def create_slot(
    slot_data: SlotCreateSchema,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    room_query = select(Room).where(Room.id == slot_data.room_id)
    room_result = await db.execute(room_query)
    room = room_result.scalar_one_or_none()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанная комната не найдена"
        )

    new_slot = Slot(
        room_id=slot_data.room_id,
        start_time=slot_data.start_time,
        end_time=slot_data.end_time,
        is_booked=False
    )
    db.add(new_slot)
    await db.commit()
    await db.refresh(new_slot)

    return new_slot


@router.get("/{room_id}/slots")
async def get_available_slots(
    room_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    query = select(Slot).where(Slot.room_id == room_id, not Slot.is_booked)
    result = await db.execute(query)
    slots = result.scalars().all()
    return slots