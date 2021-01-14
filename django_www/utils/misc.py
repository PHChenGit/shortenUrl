import random
import socket
import string
import struct
from functools import wraps
from time import time

from utils.logger import log

try:
    import simplejson as json
except Exception:
    import json


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        log.info('timeit|%s|spent:%s', func.__name__, t2 - t1)
        return result

    return wrapper


def get_client_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[0].strip()
    else:
        ipaddress = request.META.get('HTTP_X_REAL_IP')
    return ipaddress


def random_string(length=10):
    """
    Generate a random string of letters and digits
    """

    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def to_json(data, ensure_ascii=False, ensure_bytes=False):
    result = json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'))
    if ensure_bytes and isinstance(result, str):
        result = result.encode('utf-8')
    return result


def from_json(s):
    return json.loads(s)


def from_json_safe(s):
    try:
        return json.loads(s)
    except Exception:
        return None


_slash_escape = '\\/' in to_json('/')


def to_json_html_safe(obj, **kwargs):
    rv = (
        to_json(obj, **kwargs)
        .replace('<', '\\u003c')
        .replace('>', '\\u003e')
        .replace('&', '\\u0026')
        .replace("'", '\\u0027')
        .replace('\u2028', '\\u2028')
        .replace('\u2029', '\\u2029')
    )
    if _slash_escape:
        rv = rv.replace('\\/', '/')
    return rv
