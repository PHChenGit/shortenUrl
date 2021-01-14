from unittest.mock import patch

from django.test import SimpleTestCase

from django_www.services import shorten_url_service
from django_www.models import Shortenurl
from utils import exceptions, messages


class CreateUrlTestCase(SimpleTestCase):
    url = ''
    scheme = ''

    def setUp(self) -> None:
        self.fake_create_db_manager = patch('django_www.db_manager.create').start()
        self.fake_get_original_url_from_cache = patch('django_www.cache_manager.get_original_url').start()
        self.fake_update_get_original_url_from_cache = patch('django_www.cache_manager.get_original_url.update').start()
        self.fake_code_generator = patch('utils.misc.random_string').start()

    def tearDown(self) -> None:
        patch.stopall()

    def when_is_invalid_url(self):
        self.given_url('dev-shorten.com')
        self.given_scheme('')
        self.should_raise_exception()

    def when_is_valid_url(self):
        origin_url = 'https://cloud.google.com/kubernetes-engine/docs/concepts/configmap?hl=zh-cn'
        self.given_url(origin_url)
        self.given_scheme('https')
        fake_code = 'xV34f'
        self.fake_code_generator.return_value = fake_code
        self.fake_get_original_url_from_cache = None
        fake_shorten_url = f'https://shortenurl.work.tw/{fake_code}'
        self.fake_create_db_manager.return_value = Shortenurl(
            origin_url=origin_url,
            shorten_url=fake_shorten_url,
            code=fake_code,
        )
        self.fake_update_get_original_url_from_cache.return_value = {
            'origin_url': origin_url,
            'shorten_url': fake_shorten_url,
            'code': fake_code,
        }

    def should_raise_exception(self):
        with self.assertRaises(exceptions.ParseShortenUrlException) as cm:
            shorten_url_service.create_url(self.url, self.scheme)
        return cm

        the_exception = cm.exception
        self.assertEqual(messages.ERROR__INVALID_PARAMS, the_exception.msg)

    def given_url(self, url: str):
        self.url = url

    def given_scheme(self, scheme: str):
        self.scheme = scheme
