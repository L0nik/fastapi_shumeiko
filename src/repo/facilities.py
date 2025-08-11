from src.models.facilities import FacilitiesModel
from src.schemas.facilities import Facility
from src.repo.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    schema = Facility