from injector import inject

from src.commons.exception import ArgumentNullOrEmptyError, BusinessRuleError, NotFoundError
from src.repositories.stat_repository import StatRepository

from src.services.base_service import BaseService
from src.utils.config_util import ConfigUtil

from src.schemas.stat_schema import StatItemSchema, PaginationResponseStatSchema, PaginationRequestStatSchema

import math


class StatService(BaseService):

    @inject
    def __init__(self, stat_repository: StatRepository, config: ConfigUtil):
        super().__init__()
        self._stat_repository = stat_repository

    def list(self, pagination_request_stat_schema: PaginationRequestStatSchema) \
            -> PaginationResponseStatSchema:



        if pagination_request_stat_schema is None:
            raise ArgumentNullOrEmptyError("module.stat.schema_is_null", "schema is null.")

        predicate = {}

        if 'stat_period' in pagination_request_stat_schema and \
                pagination_request_stat_schema['stat_period'] is not None:
            predicate["stat_period"] = pagination_request_stat_schema["stat_period"]

        if 'stat_type' in pagination_request_stat_schema and \
                pagination_request_stat_schema['stat_type'] is not None:
            predicate["stat_type"] = pagination_request_stat_schema["stat_type"]

        count = self._stat_repository.count(predicate=predicate)



        print("count ", count)

        pagination = self.paginate(pagination_request_stat_schema)

        if count == 0:
            schema = PaginationResponseStatSchema().serialize(pagination)
            return schema

        pagination["total"] = count
        pagination["pages"] = math.ceil(count / pagination["per_page"])

        result = self._stat_repository.get_all(
            predicate=predicate,
            fields=StatItemSchema().get_fields(),
            limit=pagination["limit"],
            skip=pagination["skip"],
            sort="_id"
        )

        res = list(result)

        pagination["items"] = res

        schema = PaginationResponseStatSchema().serialize(pagination)
        return schema
