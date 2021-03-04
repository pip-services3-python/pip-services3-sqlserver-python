# -*- coding: utf-8 -*-
from pip_services3_commons.config import ConfigParams

from pip_services3_sqlserver.connect.SqlServerConnectionResolver import SqlServerConnectionResolver


class TestSqlServerConnectionResolver:

    def test_connection_config(self):
        db_config = ConfigParams.from_tuples(
            'connection.host', 'localhost',
            'connection.port', 1433,
            'connection.database', 'test',
            'connection.encrypt', True,
            'credential.username', 'sa',
            'credential.password', 'pwd#123',
        )

        resolver = SqlServerConnectionResolver()
        resolver.configure(db_config)

        uri = resolver.resolve(None)
        assert uri is not None
        assert isinstance(uri, str)
        assert 'mssql://sa:pwd#123@localhost:1433/test?encrypt=True' == uri
