import hashlib
import json
import os
import logging

import yaml


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))

def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def get_app_config():
    return load_config(os.environ.get("APP_CONFIG"))


def make_hash_from_dictionary(dct):
    text = json.dumps(dct)

    hash_object = hashlib.md5(text.encode())
    md5_hash = hash_object.hexdigest()

    return md5_hash


def logging_messages(msg, type="info", *args, **kwargs):
    if type == "info":
        logging.info(msg, *args, **kwargs)
    elif type == "error":
        logging.error(msg, *args, **kwargs)
    elif type == "warning":
        logging.warning(msg, *args, **kwargs)


