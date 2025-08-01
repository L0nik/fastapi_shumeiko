
from src.repo.base import BaseRepository
from src.models.bookings import BookingsModel
from src.schemas.bookings import Booking

class BookingsRepository(BaseRepository):
    model = BookingsModel
    schema = Booking
