from __future__ import annotations
from typing import Optional

from django_www import db_manager
from utils import exceptions
from utils.cache import cached_get, ShortenUrlCache


@cached_get(ShortenUrlCache.prefix, ShortenUrlCache.expire)
def get_original_url(code: str) -> Optional[dict]:
    url = db_manager.get_original_url(code)

    if not url:
        return None

    return url.to_dict()
