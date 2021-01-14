from functools import wraps
from typing import Tuple

from django.conf import settings
from django.core.cache import cache

SESSION_KEY__LOGIN_INFO = 'login_info'


class Expire:
    # second
    ONE_SECOND = 1
    FIFTEEN_SECONDS = ONE_SECOND * 15
    THIRTY_SECONDS = ONE_SECOND * 30
    # minute
    ONE_MINUTE = ONE_SECOND * 60
    FIVE_MINUTES = ONE_MINUTE * 5
    TEN_MINUTES = ONE_MINUTE * 10
    THIRTY_MINUTES = ONE_MINUTE * 30
    # hour
    ONE_HOUR = ONE_MINUTE * 60
    # day
    ONE_DAY = ONE_HOUR * 24
    TWO_WEEKS = ONE_DAY * 14
    THIRTY_DAYS = ONE_DAY * 30


def cached_get(cache_key_base: str, expiry: int, key_params_index: Tuple[int, ...] = tuple()):
    """
    Usage:
    @cached_get('some-key-prefix', 60)
    def my_cacheable_func(arg1, arg2):
        return 'hello world!'

    update:
    my_cacheable_func.update(arg1, arg2, result=set_result)
    if result is given, it will set the value into cache, otherwise use my_cacheable_func return

    clear:
    my_cacheable_func.clear(arg1, arg2)
    clear the cache

    :param cache_key_base: cache key base
    :param expiry: in seconds
    :param key_params_index: indexes of args that will be appended to the key base to form the key; if [], use all the args
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = generate_cache_key(cache_key_base, key_params_index, *args)
            result = cache.get(cache_key, None)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, expiry * settings.USE_CACHE)
            return result

        def update(*args, **kwargs):
            result = kwargs.get('result')
            if result is not None:
                del kwargs['result']
            else:
                result = func(*args, **kwargs)
            cache_key = generate_cache_key(cache_key_base, key_params_index, *args)
            cache.set(cache_key, result, expiry * settings.USE_CACHE)
            return result

        def clear(*args, **_):
            cache_key = generate_cache_key(cache_key_base, key_params_index, *args)
            cache.delete(cache_key)

        def clear_all():
            cache.delete_pattern(f'*{cache_key_base}*')

        wrapper.update = update
        wrapper.clear = clear
        wrapper.clear_all = clear_all
        return wrapper

    return decorator


def generate_cache_key(base, key_params_index, *args):
    if args:
        if key_params_index:
            args = [args[idx] for idx in key_params_index]
        # All values in `args` must be string hashable
        appends = [str(a) for a in args]
        return f'{base}_{"_".join(appends)}'
    return base


class Locker:
    """
    try:
        with Locker('some_key'):
        # logic implementation

    except Locker.AcquireLockError:
        # handle exception
    """

    class AcquireLockError(Exception):
        pass

    def __init__(self, key, locktimeout=10, failmsg=''):
        self.key = '[lock][%s]' % key
        self.locktimeout = locktimeout
        self.failmsg = failmsg

    def __enter__(self):
        if cache.add(self.key, True, self.locktimeout):
            return self
        raise Locker.AcquireLockError()

    def __exit__(self, exception_type, value, traceback):
        cache.delete(self.key)


class CacheKey:
    prefix = None
    help_text = None

    @classmethod
    def get_key(cls, *args):
        append_str = '_'.join([str(arg) for arg in args])
        return f'{cls.prefix}_{append_str}' if append_str else cls.prefix

    @classmethod
    def get_info(cls):
        return {
            'prefix': cls.prefix,
            'help_text': cls.help_text,
        }


class ShortenUrlCache(CacheKey):
    prefix = 'shorten_url'
    help_text = '{code}'
    expire = Expire.ONE_DAY
