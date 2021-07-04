from src.utils.dict_util import get_value


class ConfigUtil:
    def __init__(self):
        pass

    def get(self, key: str, default=None):
        return get_value(key, self.__dict__, default)
