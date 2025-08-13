from sqlalchemy import delete, select

from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.schemas.facilities import Facility, RoomFacility
from src.repo.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacility

    async def delete(self, room_id: int, facilities_ids: list[int]):
        rooms_facilities_to_delete = select(self.model).filter_by(room_id=room_id).cte("rooms_facilities_to_delete")
        delete_stmt = (
            delete(self.model)
            .filter(self.model.facility_id.in_(facilities_ids))
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(delete_stmt)