from src.repositories.base_repository import BaseRepository


class LastTransactionsRepository(BaseRepository):
    def __init__(self):
        super().__init__("last_transactions")
