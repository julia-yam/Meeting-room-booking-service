from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.models import Booking, Slot, User
from src.models.database import get_async_session
from src.routers.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

class BookingCreateSchema(BaseModel):
    slot_id: int

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreateSchema,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    slot_query = select(Slot).where(Slot.id == booking_data.slot_id)
    slot_result = await db.execute(slot_query)
    slot = slot_result.scalar_one_or_none()

    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный временльной слот не найден"
        )

    if slot.is_booked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Этот слот уже забронирован другим пользователем"
        )

    slot.is_booked = True

    new_booking = Booking(
        user_id=current_user.id,
        slot_id=slot.id
    )
    
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    return {"message": "Слот успешно забронирован", "booking_id": new_booking.id}


@router.get("/my")
async def get_my_bookings(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    query = (
        select(Booking)
        .where(Booking.user_id == current_user.id)
        .options(joinedload(Booking.slot))
    )
    result = await db.execute(query)
    bookings = result.scalars().all()
    return bookings