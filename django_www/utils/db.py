# pylint: skip-file

import time
from copy import deepcopy
from datetime import datetime
from functools import partial

from django.conf import settings
from django.db import connections, models

LOCAL_TZ = settings.CURRENT_TZ


# Custom Timestamp Field for MySQL
class TimestampField(models.DateTimeField):
    """TimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """

    def __init__(self, null=True, blank=True, **kwargs):
        super(TimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True  # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        _type = ['TIMESTAMP']
        if not self.blank:
            _type += ['default CURRENT_TIMESTAMP']
        if self.isnull:
            _type += ['NULL']
        if self.auto_now:
            _type += ['on update CURRENT_TIMESTAMP']
        return ' '.join(_type)

    def from_db_value(self, value, expression, connection):
        if isinstance(value, int):
            return datetime.fromtimestamp(value, tz=LOCAL_TZ)
        else:
            # using "replace" will cause 6-min daylight saving time issue
            # return value.replace(tzinfo=LOCAL_TZ) if value else None
            return datetime.strptime(datetime.strftime(value, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').astimezone(LOCAL_TZ) if value else None

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        try:
            if isinstance(value, str):
                return time.strftime('%Y-%m-%d %H:%M:%S', datetime.strptime(value, '%Y-%m-%d %H:%M:%S').astimezone(LOCAL_TZ).timetuple())
            return time.strftime('%Y-%m-%d %H:%M:%S', value.astimezone(LOCAL_TZ).timetuple())
        except ValueError:
            return time.strftime('%Y-%m-%d %H:%M:%S', value.replace(tzinfo=LOCAL_TZ).timetuple())


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        return 'TINYINT'

    def formfield(self, **kwargs):
        defaults = {'min_value': -128, 'max_value': 127}
        defaults.update(kwargs)
        return super(TinyIntegerField, self).formfield(**defaults)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        return 'TINYINT UNSIGNED'

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': 255}
        defaults.update(kwargs)
        return super(PositiveTinyIntegerField, self).formfield(**defaults)


class PositiveAutoField(models.AutoField):
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'INT UNSIGNED AUTO_INCREMENT'
        return super(PositiveAutoField, self).db_type(connection)

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': 2 ** 32 - 1}
        defaults.update(kwargs)
        return super(PositiveAutoField, self).formfield(**defaults)


class PositiveBigIntegerField(models.BigIntegerField):
    empty_strings_allowed = False

    def db_type(self, connection):
        return 'BIGINT UNSIGNED'

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': models.BigIntegerField.MAX_BIGINT * 2 + 1}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)


class BigAutoField(models.AutoField):
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'BIGINT AUTO_INCREMENT'
        return super(BigAutoField, self).db_type(connection)

    def formfield(self, **kwargs):
        defaults = {'min_value': -models.BigIntegerField.MAX_BIGINT - 1, 'max_value': models.BigIntegerField.MAX_BIGINT}
        defaults.update(kwargs)
        return super(BigAutoField, self).formfield(**defaults)


class PositiveBigAutoField(models.AutoField):
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'BIGINT UNSIGNED AUTO_INCREMENT'
        return super(PositiveBigAutoField, self).db_type(connection)

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': models.BigIntegerField.MAX_BIGINT * 2 + 1}
        defaults.update(kwargs)
        return super(PositiveBigAutoField, self).formfield(**defaults)


class MySQLCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'CHAR(%s)' % self.max_length
        return super(MySQLCharField, self).db_type(connection)


class BaseModel(models.Model):
    def update_with_fields(self, data: dict):
        d = deepcopy(data)
        if 'id' in d:  # don't update `id` field
            d.pop('id')
        for key, val in d.items():  # update multiple fields on a django model instance
            setattr(self, key, val)
        # must include `updated_at` for auto_now
        self.save(update_fields=list(d.keys()) + ['updated_at'])
        return self

    id = models.AutoField(primary_key=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Time', help_text=settings.TIME_ZONE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Time', help_text=settings.TIME_ZONE)

    objects = models.Manager()

    class Meta:
        abstract = True


class DatabaseRouter(object):
    """Allows each model to set its own destiny"""

    def db_for_read(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return 'default'

    def db_for_write(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return 'default'

    def allow_syncdb(self, db, model):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def close_connections():
    for conn in connections.all():
        conn.close()


foreign_key_of = partial(models.ForeignKey, db_constraint=False, on_delete=models.DO_NOTHING, null=True)
one_to_one_field_of = partial(models.OneToOneField, db_constraint=False, on_delete=models.DO_NOTHING)
