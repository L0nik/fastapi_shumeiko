from fastapi import APIRouter, Request, HTTPException
from datetime import date

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.auth import AuthService
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("", summary="забронировать номер")
async def post_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
    request: Request
):
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room_data:
        raise HTTPException(status_code=404, detail="Номер с таким идентификатором не найден")
    _booking_data = BookingAdd(
        user_id=user_id,
        hotel_id=room_data.hotel_id,
        price=room_data.price,
        **booking_data.model_dump()
    )
    new_booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": new_booking}