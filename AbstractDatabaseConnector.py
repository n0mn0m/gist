"""
 An Abstract Base Class OOP example building on prior example for Code Louisville Fall 2017 
"""

import sqlite3
import pdb
from abc import ABCMeta, abstractmethod

class DatabaseConnector(metaclass=ABCMeta):
    """A class to help you connect to various databases"""

    __metaclass__ = ABCMeta
    _max_connections = 3
    _current_connections = 0

    def __init__(self, server, database, schema):
        self.server = server,
        self.database = database,
        self.schema = schema,
        self._timeout = None

        self._increment_current_connections()

        if self._current_connections > self._max_connections:
            print("""MAX CONNECTIONS: {0} CURRENT CONNECTIONS: {1}\n
                   Please close a connection to create a new one.""")
            raise Exception

    @property
    def timeout(self):
        return self.timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @abstractmethod
    def execute_query(self):
        raise NotImplementedError()

    #@abstractmethod
    def bulk_export(self):
        raise NotImplementedError()

    @staticmethod
    def sql_syntax_help():
        print("SELECT {COLUMNS} FROM {TABLE_NAME}\
               \nSELECT {COLUMNS} FROM {SCHEMA}.{TABLE} WHERE {CONDITIONAL}\
               \nSELECT {COLUMNS} FROM {SCHEMA}.{TABLE} WHERE {CONDITIONAL} ORDER BY {COLUMN} {ASC\DESC}\
               \nSELECT {AGGREGATE FUNCTION} {COLUMN} FROM {SCHEMA}.{TABLE}")


    @classmethod
    def _increment_current_connections(cls):
        cls._current_connections += 1

    @classmethod
    def _decrement_current_connections(cls):
        cls._current_connections -= 1

    @classmethod
    def update_max_connections(cls, count):
        cls._max_connections = count


class SQLLiteDatabaseConnector(DatabaseConnector):
    def __init__(self, server, database, schema):
        super(self.__class__, self).__init__(server, database, schema)
        self._connection = None
        self.type = 'sqlite3'

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection_string):
        self._connection = sqlite3.connect(connection_string).cursor()

    @connection.deleter
    def connection(self):
        pdb.set_trace()
        self._connection.close()
        del self._connection
        self._decrement_current_connections()
        pdb.set_trace()

    def execute_query(self, query):
        query_result = []
        result = self._connection.execute(query)
        [query_result.append(r) for r in result]
        return query_result

class MSSqlDatabaseConnection(DatabaseConnector):
    def init(self, server, database, schema):
        super(MSSqlDatabaseConnection, self).__init__(server, database, schema)
        self.type = 'mssql'


if __name__ == "__main__":
    chinook = SQLLiteDatabaseConnector("localhost", "chinook.db", None)
    chinook.connection = 'chinook.db'
    data = chinook.execute_query("SELECT * FROM artists")
    [print(row) for row in data]
    del chinook.connection
    chinook.sql_syntax_help()
