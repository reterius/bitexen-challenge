from injector import inject
from src.repositories.base_repository import BaseRepository
from src.utils.config_util import ConfigUtil
from src.utils.dict_util import get_value


class StatRepository(BaseRepository):

    @inject
    def __init__(self, config: ConfigUtil):
        super().__init__(collection_name="statistics",
                         db_dsn=get_value("dsn", config.get("MONGODB")),
                         db_name=get_value("name", config.get("MONGODB")),
                         username=get_value("username", config.get("MONGODB")),
                         password=get_value("password", config.get("MONGODB")),
                         )
