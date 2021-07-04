from marshmallow import fields, validate

from src.schemas.base_schema import BaseSchema, default_error_messages

PAGINATION_PER_PAGE_LENGTH_DEFAULT = 25


class PaginationRequestSchema(BaseSchema):
    page = fields.Int(
        required=False,
        validate=[validate.Range(min=1, max=10000000)],
        allow_none=False,
        default=1,
        error_messages=default_error_messages
    )

    per_page = fields.Int(
        required=False,
        validate=[
            validate.Range(min=1, max=10000),

        ],
        allow_none=False,
        default=PAGINATION_PER_PAGE_LENGTH_DEFAULT,
        error_messages=default_error_messages
    )


class PaginationResponseSchema(BaseSchema):
    page = fields.Int(
        required=True,
        allow_none=False,
        error_messages=default_error_messages
    )

    per_page = fields.Int(
        required=True,
        allow_none=False,
        error_messages=default_error_messages
    )

    total = fields.Int(
        required=True,
        allow_none=False,
        error_messages=default_error_messages
    )

    pages = fields.Int(
        required=True,
        allow_none=False,
        error_messages=default_error_messages
    )

