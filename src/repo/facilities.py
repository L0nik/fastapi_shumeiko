from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.schemas.facilities import Facility, RoomFacility
from src.repo.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacility