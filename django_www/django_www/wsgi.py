import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_www.settings')


try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass

application = get_wsgi_application()
