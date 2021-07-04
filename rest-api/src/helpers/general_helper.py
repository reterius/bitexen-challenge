import re
import requests
import json
import unidecode


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def lreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)


def rreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' ends 'string'.
    """
    return re.sub('%s$' % pattern, sub, string)


def call_api(method="POST", endpoint="", params=None):
    response = None
    if method == "GET":
        response = requests.get(endpoint, params)
    elif method == "POST":
        response = requests.post(endpoint, params)

    return response


def print_dict_to_json_nicely(dict):
    res = json.dumps(dict)
    res = json.loads(res)
    res = json.dumps(res, indent=4, sort_keys=True)
    return res


def stripHTMLTags(html):
    """
      Strip HTML tags from any string and transfrom special entities
    """
    import re
    text = html

    # apply rules in given order!
    rules = [
        {r'>\s+': u'>'},  # remove spaces after a tag opens or closes
        {r'\s+': u' '},  # replace consecutive spaces
        {r'\s*<br\s*/?>\s*': u'\n'},  # newline after a <br>
        {r'</(div)\s*>\s*': u'\n'},  # newline after </p> and </div> and <h1/>...
        {r'</(p|h\d)\s*>\s*': u'\n\n'},  # newline after </p> and </div> and <h1/>...
        {r'<head>.*<\s*(/head|body)[^>]*>': u''},  # remove <head> to </head>
        {r'<a\s+href="([^"]+)"[^>]*>.*</a>': r'\1'},  # show links instead of texts
        {r'[ \t]*<[^<]*?/?>': u' '},  # remove remaining tags
        {r'^\s+': u''}  # remove spaces at the beginning
    ]

    for rule in rules:
        for (k, v) in rule.items():
            regex = re.compile(k)
            text = regex.sub(v, text)

    # replace special strings
    special = {
        '&nbsp;': ' ', '&amp;': '&', '&quot;': '"',
        '&lt;': '<', '&gt;': '>'
    }

    for (k, v) in special.items():
        text = text.replace(k, v)
    return text


def check_address_type(address):
    type = "world-wide-web"
    onions = list(re.finditer(r'(?:https?://)?(?:www)?(\S*?\.onion)\b', address, re.M | re.IGNORECASE))
    if len(onions) > 0:
        type = "deep-web"

    return type


def generate_cache_key(predicate: dict, _collection_name: str) -> str:

    if '_id' in predicate:
        predicate["_id"] = str(predicate['_id'])

    cache_key_dict = {k: v for k, v in predicate.items()}
    cache_key_dict['_collection_name'] = _collection_name
    return json.dumps(cache_key_dict)


def get_difference_lists(l1, l2):
    diff = list(set(l1) - set(l2))
    return diff


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)
