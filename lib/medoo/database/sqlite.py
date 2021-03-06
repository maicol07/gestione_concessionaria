import sqlite3

from lib import six
from ..base import Base
from ..dialect import Dialect


class DialectSqlite(Dialect):

    @staticmethod
    def value(item):
        if isinstance(item, six.string_types):
            return "'%s'" % item.replace("'", "''")
        # return "'{}'".format(item.replace("'", "''"))
        elif isinstance(item, bool):
            return str(int(item))
        elif item is None:
            return 'NULL'
        return str(item)


class Sqlite(Base):

    def __init__(self, *args, **kwargs):
        database = kwargs.pop('database', kwargs.pop('database_file', None))
        if database is not None and database.startswith('file://'):
            database = database.replace('file://', '')
        kwargs['database'] = database
        super(Sqlite, self).__init__(*args, **kwargs)
        self.cursor = self.connection.cursor()
        self.dialect(DialectSqlite)

    def _connect(self, *args, **kwargs):
        if kwargs['database']:
            database = kwargs['database']
        else:
            database = ':memory:'
        arguments = {
            'database': database,
            'timeout': 5.0,
            'detect_types': 0,
            'isolation_level': None,
            'check_same_thread': False,
            'cached_statements': 100,

            # 'factory'      : [str][0],
        }

        return sqlite3.connect(**arguments)
