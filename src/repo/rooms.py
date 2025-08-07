from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel
from src.repo.base import BaseRepository
from src.schemas.rooms import Room
from src.repo.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        return await self.get_filtered(RoomsModel.id.in_(rooms_ids_to_get))