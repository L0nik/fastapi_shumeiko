from sqlalchemy import select, func
from datetime import date

from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repo.base import BaseRepository
from src.schemas.hotels import Hotel
from src.repo.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    async def get_all(
        self,
        location,
        title,
        limit,
        offset
    ) -> list[Hotel]:
        query = select(HotelsModel)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsModel.hotel_id).
            select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )

        filter_query = select(HotelsModel.id).select_from(HotelsModel)

        if location:
            filter_query = filter_query.filter(func.lower(HotelsModel.location).contains(location.lower()))
        if title:
            filter_query = filter_query.filter(func.lower(HotelsModel.title).contains(title.lower()))

        return await self.get_filtered(HotelsModel.id.in_(hotels_ids_to_get), HotelsModel.id.in_(filter_query), limit=limit, offset=offset,)