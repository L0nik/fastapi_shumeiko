from sqlalchemy import select, insert, func

from src.models.hotels import HotelsModel
from src.repo.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(
        self,
        location,
        title,
        limit,
        offset
    ):
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
        return result.scalars().all()