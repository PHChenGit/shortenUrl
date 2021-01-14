from django.db import models

from utils.db import BaseModel


class Shortenurl(BaseModel):
    origin_url = models.URLField(max_length=255)
    shorten_url = models.URLField(max_length=255, unique=True)
    code = models.CharField(max_length=8, unique=True)

    class Meta:
        db_table = 'shorten_url'
        unique_together = [['origin_url', 'shorten_url']]

    def to_dict(self) -> dict:
        return {
            'origin_url': self.origin_url,
            'shorten_url': self.shorten_url,
            'code': self.code,
        }
