from marshmallow import fields, validate
from src.schemas.base_schema import default_error_messages, BaseSchema
from src.schemas.pagination_schema import PaginationRequestSchema, PaginationResponseSchema







class PaginationRequestStatSchema(PaginationRequestSchema):
    stat_period = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )

    stat_type = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )


class StatItemSchema(BaseSchema):
    _id = fields.Str()

    stat_period = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )

    date_key = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )

    last_calculated_date = fields.DateTime(
        required=False,
        default=None,
        allow_none=True,
        format="%Y-%m-%d %H:%M:%S.%f",
        error_messages=default_error_messages,
    )

    stat_type = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )

    quantity = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    total_amount_count = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    year = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    month = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    week = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )


    day = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )



class AddStatSchema(BaseSchema):

    stat_period = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )

    date_key = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )


    stat_type = fields.Str(
        required=False,
        allow_none=True,
        error_messages=default_error_messages
    )

    quantity = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    total_amount_count = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    year = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    month = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )

    week = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )


    day = fields.Int(
        required=False,
        default=0,
        error_messages=default_error_messages,
    )







class PaginationResponseStatSchema(PaginationResponseSchema):
    items = fields.List(fields.Nested(
        StatItemSchema,
        default=None,
        error_messages=default_error_messages,
    ))


