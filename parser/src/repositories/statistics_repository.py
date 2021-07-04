from src.repositories.base_repository import BaseRepository


class StatisticsRepository(BaseRepository):
    def __init__(self):
        super().__init__("statistics")
