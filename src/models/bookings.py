import datetime
from sqlalchemy import ForeignKey, String, Date, Time, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.models.users import User

class Room(Base):
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True) 
    
    slots: Mapped[list["Slot"]] = relationship(back_populates="room", cascade="all, delete-orphan")


class Slot(Base):
    __tablename__ = "slots"

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    room: Mapped["Room"] = relationship(back_populates="slots")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="slot")


class Booking(Base):
    __tablename__ = "bookings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    user: Mapped["User"] = relationship()
    slot: Mapped["Slot"] = relationship(back_populates="bookings")