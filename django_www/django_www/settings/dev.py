# choose whether to use cache or not
CACHES = {
    'default': {
        'BACKEND': 'redis_lock.django_cache.RedisCache',
        'LOCATION': 'redis://cache1:6379',
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_TIMEOUT': 30,
            'SOCKET_CONNECT_TIMEOUT': 30,
            'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 1000,
                'timeout': 30,
            },
        },
        'KEY_PREFIX': 'dev_shorten_url_work_tw',
    },
}

# choose whether to use cache or not
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'db1',
        # os.environ.get('MYSQL_1_ENV_MYSQL_USER') doesn't have privilage to create test DB
        'USER': 'root',
        'PASSWORD': 'app',
        'NAME': 'app',
        'PORT': 3306,
        'CONN_MAX_AGE': 100,
        'OPTIONS': {'charset': 'utf8mb4', 'use_unicode': True},
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'db1',
        # os.environ.get('MYSQL_1_ENV_MYSQL_USER') doesn't have privilage to create test DB
        'USER': 'root',
        'PASSWORD': 'app',
        'NAME': 'app',
        'PORT': 3306,
        'CONN_MAX_AGE': 100,
        'TEST': {'MIRROR': 'default'},
        'OPTIONS': {'charset': 'utf8mb4', 'use_unicode': True},
    },
}

INTERNAL_IPS = ('127.0.0.1',)

USE_CACHE = 0
