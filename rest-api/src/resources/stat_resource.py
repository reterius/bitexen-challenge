from injector import inject

from src.commons.response import created_result, ok_result
from src.resources.base_resource import BaseResource
from src.schemas.stat_schema import PaginationRequestStatSchema
from src.services.stat_service import StatService


class StatResource(BaseResource):

    @inject
    def __init__(self, stat_service: StatService):
        super().__init__()
        self._stat_service = stat_service

    def get(self):
        schema = PaginationRequestStatSchema().get_with_valid_args_payload()
        result = self._stat_service.list(schema)
        return ok_result(result)
