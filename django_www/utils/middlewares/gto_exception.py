import traceback

from django.conf import settings

from utils import http_response
from utils.logger import log


class GTOExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):    # pylint: disable=no-self-use
        if settings.DEPLOY_ENV != 'dev':
            log.error('&'.join(i.strip('\n').replace('\n', '&') for i in traceback.format_exception(None, exception, exception.__traceback__)))
            return http_response.json_response_server_error(request)

        log.exception(exception)
        raise exception
