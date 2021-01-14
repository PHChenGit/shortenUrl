import os

CACHES = {
    'default': {
        'BACKEND': 'redis_lock.django_cache.RedisCache',
        'LOCATION': f'redis://{os.environ.get("REDIS_HOST")}:6379?health_check_interval=30',
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
        'KEY_PREFIX': 'shorten_url_work_tw',
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('LIVE_DB_HOST'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('LIVE_DB_PASSWORD'),
        'NAME': os.environ.get('DB_NAME'),
        'PORT': os.environ.get('DB_PORT'),
        'CONN_MAX_AGE': 3600,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('LIVE_DB_SLAVE_HOST'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('LIVE_DB_PASSWORD'),
        'NAME': os.environ.get('DB_NAME'),
        'PORT': os.environ.get('DB_PORT'),
        'CONN_MAX_AGE': 3600,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
}
