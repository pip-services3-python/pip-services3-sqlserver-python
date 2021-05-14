# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.refer import References, Descriptor

from pip_services3_sqlserver.connect.SqlServerConnection import SqlServerConnection
from test.fixtures.DummyPersistenceFixture import DummyPersistenceFixture
from test.persistence.DummySqlServerPersistence import DummySqlServerPersistence


class TestDummySqlServerConnection:
    connection: SqlServerConnection
    persistence: DummySqlServerPersistence
    fixture: DummyPersistenceFixture

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

    @classmethod
    def setup_class(cls):
        if cls.sqlserver_uri is None and cls.sqlserver_host is None:
            return

        cls.connection = SqlServerConnection()
        cls.connection.configure(cls.db_config)

        cls.persistence = DummySqlServerPersistence()
        cls.persistence.set_references(References.from_tuples(
            Descriptor("pip-services", "connection", "sqlserver", "default", "1.0"), cls.connection
        ))

        cls.fixture = DummyPersistenceFixture(cls.persistence)

        cls.connection.open(None)
        cls.persistence.open(None)

    @classmethod
    def teardown_class(cls):
        cls.connection.close(None)
        cls.persistence.close(None)

    def setup_method(self):
        self.persistence.clear(None)

    def test_connection(self):
        assert self.connection.get_connection() is not None
        assert isinstance(self.connection.get_database_name(), str)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_batch_operations(self):
        self.fixture.test_batch_operations()
