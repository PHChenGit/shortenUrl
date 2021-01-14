from functools import wraps

from django.core.cache import cache

from utils.logger import log


def locker(function):
    @wraps(function)
    def _locker(request, *args, **kwargs):
        try:
            with cache.lock('redirect_to_original_url'):
                return function(request, *args, **kwargs)
        except Exception as e:
            log.warning('locker|locker_error|err:%s', e)
            raise e
    return _locker
