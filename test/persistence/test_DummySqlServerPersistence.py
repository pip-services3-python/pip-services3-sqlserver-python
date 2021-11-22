# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams

from test.fixtures.DummyPersistenceFixture import DummyPersistenceFixture
from test.persistence.DummySqlServerPersistence import DummySqlServerPersistence


class TestDummySqlServerPersistence:
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

    def setup_method(self):
        if self.sqlserver_uri is None and self.sqlserver_host is None:
            return
        self.persistence = DummySqlServerPersistence()
        self.persistence.configure(self.db_config)

        self.fixture = DummyPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_batch_operations(self):
        self.fixture.test_batch_operations()
