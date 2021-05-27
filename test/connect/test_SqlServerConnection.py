# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams

from pip_services3_sqlserver.connect.SqlServerConnection import SqlServerConnection


class TestSqlServerConnection:
    connection: SqlServerConnection



    def setup_method(self):
        sqlserver_uri = os.getenv('SQLSERVER_URI')
        sqlserver_host = os.getenv('SQLSERVER_HOST') or 'localhost'
        sqlserver_port = os.getenv('SQLSERVER_PORT') or 1433
        sqlserver_database = os.getenv('SQLSERVER_DB') or 'master'
        sqlserver_user = os.getenv('SQLSERVER_USER') or 'sa'
        sqlserver_password = os.getenv('SQLSERVER_PASSWORD') or 'sqlserver_123'

        db_config = ConfigParams.from_tuples(
            'connection.uri', sqlserver_uri,
            'connection.host', sqlserver_host,
            'connection.port', sqlserver_port,
            'connection.database', sqlserver_database,
            'credential.username', sqlserver_user,
            'credential.password', sqlserver_password
        )
        if sqlserver_uri is None and sqlserver_host is None:
            return

        self.connection = SqlServerConnection()
        self.connection.configure(db_config)

        self.connection.open(None)

    def teardown_method(self):
        self.connection.close(None)

    def test_open_and_close(self):
        assert self.connection.get_connection() is not None
        assert isinstance(self.connection.get_database_name(), str)


