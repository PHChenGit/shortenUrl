from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase

from django_www.services import shorten_url_service
from django_www.models import Shortenurl
from utils import exceptions, messages


class GetUrlTestCase(SimpleTestCase):
    url = ''

    def setUp(self) -> None:
        self.fake_get_original_url_from_cache = patch('django_www.services.shorten_url_service.cache_manager.get_original_url').start()
        self.fake_clear_get_original_url_from_cache = patch('django_www.services.shorten_url_service.cache_manager.get_original_url.clear').start()

    def tearDown(self) -> None:
        patch.stopall()

    def when_is_invalid_shorten_url(self):
        self.url = 'https://cloud.google.com/'
        self.should_raise_exception()

    def should_raise_exception(self):
        with self.assertRaises(exceptions.ParseShortenUrlException) as cm:
            shorten_url_service.get_original_url(self.url)
        return cm

        the_exception = cm.exception
        self.assertEqual(messages.ERROR__INVALID_PARAMS, the_exception.msg)

    def when_shorten_code_not_exists(self):
        code = 'c3G91'
        self.url = f'http://{settings.DOMAIN}/{code}'
        self.fake_get_original_url_from_cache.return_value = None

        act = shorten_url_service.get_original_url(self.url)
        excepted = ''

        self.assertEqual(excepted, act)

    def when_shorten_code_exists(self):
        code = 'c3G91'
        self.url = f'http://{settings.DOMAIN}/{code}'
        original_url = 'https://cloud.google.com/kubernetes-engine/docs/concepts/configmap?hl=zh-cn'
        self.fake_get_original_url_from_cache.return_value = {
            'origin_url': original_url,
            'shorten_url': self.url,
            'code': code,
        }

        act = shorten_url_service.get_original_url(self.url)
        excepted = original_url

        self.assertEqual(excepted, act)
