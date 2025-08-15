
from src.repo.base import BaseRepository
from src.models.bookings import BookingsModel
from src.repo.mappers.mappers import BookingDataMapper

class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper
