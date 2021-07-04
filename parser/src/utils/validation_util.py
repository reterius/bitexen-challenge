
def is_null(value):
    return value is None


def is_empty(value):
    return is_equals(value, '')


def is_null_or_empty(value):
    return is_null(value) or is_empty(value)


def is_equals(value, predicate):
    return value == predicate


def is_not_equals(value, predicate):
    return value != predicate


def has_length(value, predicate):
    return len(value) == predicate


def has_min_length(value, predicate):
    return len(value) < predicate


def has_max_length(value, predicate):
    return len(value) > predicate


def has_range_length(value, predicate_min, predicate_max):
    return has_min_length(value, predicate_min) and has_max_length(value, predicate_max)


def is_email_address(value: str):
    return True


def is_ipv4_address(value: str):
    return True


def is_ipv6_address(value: str):
    return True


def is_url(value: str):
    return True


def is_fqdn(value: str):
    return True


def is_md5(value: str):
    return True


def is_sha1(value: str):
    return True

