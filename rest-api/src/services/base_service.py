from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from src.commons.exception import ArgumentNullOrEmptyError


class BaseService:

    def __init__(self):
        pass

    def paginate(self, pagination_request_schema, total_count: int = 0) -> dict:
        """
        pagination işlermlerinde pagination_request_schema kullanılan request objeleri için limit ve skip değerlerini geri döner.
        :param pagination_request_schema: PaginationRequestSchema objesinden kalıtılmalıdır
        :return: limit(per_page), skip ve page parametreleri döner
        """

        page = 1
        per_page = 10

        if "page" in pagination_request_schema:
            page = pagination_request_schema["page"]

        if "per_page" in pagination_request_schema:
            per_page = pagination_request_schema["per_page"]

        skip = (page - 1) * per_page
        # return per_page, skip, page

        data = {
            "page": page,
            "per_page": per_page,
            "total": total_count,
            "pages": 0,
            "items": [],

            "limit": per_page,
            "skip": skip,
        }

        return data
