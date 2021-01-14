import re

from django.conf import settings
from django.http import HttpRequest

from django_www import cache_manager, db_manager
from utils import exceptions, messages, misc


def create_url(origin_url: str, scheme: str) -> str:
    match = re.search(f'^http(s)?:\/\/(www.)?[a-zA-Z0-9.\/%-@_&=#]*', origin_url)

    if not match or len(origin_url) > 255:
        raise exceptions.ParseShortenUrlException(messages.ERROR__INVALID_PARAMS)

    while True:
        code = misc.random_string(5)
        url = cache_manager.get_original_url(code)
        if not url:
            break

    new_url = db_manager.create({'origin_url': origin_url, 'shorten_url': f'{scheme}://{settings.DOMAIN}/{code}', 'code': f'{code}'})
    cache_manager.get_original_url.update(code, result=new_url)
    return new_url.shorten_url


def get_original_url(shorten_url: str) -> str:
    base_validator(shorten_url)
    s = shorten_url.split(f'{settings.DOMAIN}/')
    code = s[1]

    if len(code) > 5 and code[-1] == '/':
        code = code[:6]

    url = cache_manager.get_original_url(code)

    if not url:
        cache_manager.get_original_url.clear(code)
        return ''

    return url.get('origin_url')


def base_validator(url: str) -> None:
    domain = ''

    for ch in settings.DOMAIN:
        if ch == '.':
            domain += '\\'
        domain += ch

    pattern = '^http(s)?:\/\/%s\/[a-zA-Z0-9]{5}\/?$' % domain
    match = re.search(pattern, url)

    if not match:
        raise exceptions.ParseShortenUrlException(messages.ERROR__INVALID_CODE)
