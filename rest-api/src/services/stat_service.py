from bson import ObjectId
from injector import inject

from src.commons.exception import ArgumentNullOrEmptyError, BusinessRuleError, NotFoundError
from src.repositories.stat_repository import StatRepository

from src.services.base_service import BaseService
from src.utils.config_util import ConfigUtil

from src.schemas.stat_schema import StatItemSchema, PaginationResponseStatSchema, PaginationRequestStatSchema, \
    AddStatSchema

import math

from src.utils.validation_util import is_null_or_empty


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

        print("predicate ", predicate)

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

    def delete_by_id(self, _id):

        schema = StatItemSchema()

        predicate = {
            "_id": ObjectId(_id)
        }

        result = self._stat_repository.remove(
            predicate=predicate,
        )

        if result is None:
            raise NotFoundError("module.stat.not_found", "report not found.")

        result = schema.serialize(result)
        return result

    def add(self, schema: AddStatSchema):

        if is_null_or_empty(schema):
            raise ArgumentNullOrEmptyError("module.address_actions.schema_is_null", "schema is null.")

        add_report_dict = {

            "stat_period": schema["stat_period"],
            "date_key": schema["date_key"],

            "stat_type": schema["stat_type"],
            "quantity": schema["quantity"],
            "total_amount_count": schema["total_amount_count"],
            "year": schema["year"],
            "month": schema["month"],
            "week": schema["week"],
            "day": schema["day"]
        }

        self._stat_repository.add(add_report_dict)

        return add_report_dict
