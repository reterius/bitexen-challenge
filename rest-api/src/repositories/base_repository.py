from src.helpers.mongodb_helper import MongodbHelper


class BaseRepository(MongodbHelper):
    def __init__(
            self,
            collection_name: str,
            db_dsn: str,
            db_name: str,
            username: str,
            password: str,
    ):
        super().__init__(collection_name, db_dsn, db_name, username, password)
