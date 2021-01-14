from __future__ import annotations
from typing import Optional

from .models import Shortenurl


def create(data: dict) -> Shortenurl:
    return Shortenurl.objects.create(**data)


def get_original_url(code: str) -> Optional[Shortenurl]:
    return Shortenurl.objects.filter(code=code).first()
