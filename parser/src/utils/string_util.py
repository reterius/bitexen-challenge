from slugify import slugify


def create_slug(value: str) -> str:
    if not value:
        raise Exception("value is can not be null or empty")

    value = slugify(value)
    return value
