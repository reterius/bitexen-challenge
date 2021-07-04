from src.helpers.general_helper import get_app_config
from src.helpers.mongodb_helper import MongodbHelper

import os
import json

app_config = get_app_config()

class BaseRepository(MongodbHelper):
    def __init__(
            self,
            collection_name: str,
            db_dsn: str = app_config['mongo_db']['dsn'],
            db_name: str = app_config['mongo_db']['db_name'],
            username: str = app_config['mongo_db']['username'],
            password: str = app_config['mongo_db']['password']
    ):
        super().__init__(collection_name, db_dsn, db_name, username, password)
