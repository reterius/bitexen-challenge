from injector import inject

from src.commons.response import created_result, ok_result
from src.resources.base_resource import BaseResource
from src.schemas.stat_schema import PaginationRequestStatSchema, AddStatSchema
from src.services.stat_service import StatService


class StatResource(BaseResource):

    @inject
    def __init__(self, stat_service: StatService):
        super().__init__()
        self._stat_service = stat_service

    def get(self):
        schema = PaginationRequestStatSchema().get_with_valid_args_payload()

        print("request schema ", schema)

        result = self._stat_service.list(schema)
        return ok_result(result)

    def post(self):
        schema = AddStatSchema().get_with_valid_json_payload()

        print("schema ", schema)


        result = self._stat_service.add(schema)
        return ok_result(result)


class StatItemResource(BaseResource):

    @inject
    def __init__(self, stat_service: StatService):
        super().__init__()
        self._stat_service = stat_service

    def delete(self, _id):
        result = self._stat_service.delete_by_id(_id=_id)
        return ok_result(result)
