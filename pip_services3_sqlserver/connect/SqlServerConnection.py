# -*- coding: utf-8 -*-

import urllib.parse as urlparse
from typing import Optional, Any

import pyodbc
from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.errors import ConnectionException
from pip_services3_commons.refer import IReferenceable, IReferences
from pip_services3_commons.run import IOpenable
from pip_services3_components.log import CompositeLogger

from pip_services3_sqlserver.connect.SqlServerConnectionResolver import SqlServerConnectionResolver


class SqlServerConnection(IReferenceable, IConfigurable, IOpenable):
    """
    SqlServer connection using plain driver.

    By defining a connection and sharing it through multiple persistence components
    you can reduce number of used database connections.

    ### Configuration parameters ###
        - connection(s):
            - discovery_key:             (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`
            - host:                      host name or IP address
            - port:                      port number (default: 27017)
            - uri:                       resource URI or connection string with all parameters in it
        - credential(s):
            - store_key:                 (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>`
            - username:                  user name
            - password:                  user password
        - options:
            - connect_timeout:      (optional) number of milliseconds to wait before timing out when connecting a new client (default: 0)
            - idle_timeout:         (optional) number of milliseconds a client must sit idle in the pool and not be checked out (default: 10000)
            - max_pool_size:        (optional) maximum number of clients the pool should contain (default: 10)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages components to pass log messages
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` services
        - `*:credential-store:*:*:1.0` (optional) :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>` stores to resolve credentials
    """

    def __init__(self):
        """
        Creates a new instance of the connection component.
        """
        self.__default_config = ConfigParams.from_tuples(
            # connections. *
            # credential. *

            "options.connect_timeout", 15000,
            "options.request_timeout", 15000,
            "options.idle_timeout", 30000,
            "options.max_pool_size", 3
        )

        # The logger.
        self._logger: CompositeLogger = CompositeLogger()
        # The connection resolver.
        self._connection_resolver: SqlServerConnectionResolver = SqlServerConnectionResolver()
        # The configuration options.
        self._options: ConfigParams = ConfigParams()
        # The SQLServer connection pool object.
        self._connection: Any = None
        # The SQLServer database name.
        self._database_name: str = None

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        config = config.set_defaults(self.__default_config)

        self._connection_resolver.configure(config)

        self._options = self._options.override(config.get_section('options'))

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._connection_resolver.set_references(references)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._connection is not None

    def __compose_uri_settings(self, uri: str) -> str:

        settings = {
            # 'parseJSON': true,
            # 'connectTimeout': connect_timeout_MS,
            # 'requestTimeout': request_timeout_MS,
            # 'pool.min': 0,
            # 'pool.max': maxPoolSize,
            # 'pool.idleTimeoutMillis': idle_timeout_MS
        }

        params = ''
        for key in settings:
            if len(params) > 0:
                params += '&'

            params += key

            value = settings[key]
            if value is not None:
                params += '=' + value

        if uri.find('?') < 0:
            uri += '?' + params
        else:
            uri += '&' + params

        return uri

    def open(self, correlation_id: Optional[str]):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: raise error or None no errors occured.
        """
        try:
            uri = self._connection_resolver.resolve(correlation_id)
            self._logger.debug(correlation_id, "Connecting to sqlserver")

            try:
                # config = self.__compose_uri_settings(uri)

                max_pool_size = self._options.get_as_nullable_string("max_pool_size")
                connect_timeout_MS = self._options.get_as_nullable_integer("connect_timeout") or 0
                request_timeout_MS = self._options.get_as_nullable_integer("request_timeout") or 0
                # idle_timeout_MS = self._options.get_as_nullable_integer("idle_timeout") or 0

                parsed_url = urlparse.urlparse(uri)
                connect_str = 'DRIVER={ODBC Driver 17 for SQL Server};' + \
                              f'Server={parsed_url.hostname},{parsed_url.port};\
                              Database={parsed_url.path[1:]};' + \
                              f'UID={parsed_url.username};\
                                 PWD={parsed_url.password};' if parsed_url.username and parsed_url.password else 'Trusted_Connection=yes;'
                # Try to connect
                if max_pool_size:
                    pyodbc.SQL_MAX_DRIVER_CONNECTIONS = max_pool_size

                self._connection = pyodbc.connect(connect_str, timeout=int(connect_timeout_MS / 1000))
                self._connection.timeout = int(request_timeout_MS / 1000)
                cursor = self._connection.cursor()
                cursor.execute('SET ARITHABORT ON')
                cursor.commit()
                cursor.close()

                self._database_name = parsed_url.path[1:]

            except Exception as err:
                raise ConnectionException(correlation_id, "CONNECT_FAILED",
                                          "Connection to sqlserver failed").with_cause(err)

        except Exception as err:
            self._logger.error(correlation_id, err, 'Failed to resolve sqlserver connection')

    def close(self, correlation_id: Optional[str]):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: raise error or null no errors occured.
        """
        if self._connection is None:
            return
        try:
            self._connection.close()
            self._connection = None
            self._logger.debug(
                correlation_id, "Disconnected from sqlserver database %s", self._database_name)
        except Exception as err:
            ConnectionException(correlation_id, 'DISCONNECT_FAILED',
                                'Disconnect from sqlserver failed: ').with_cause(err)

        self._connection = None
        self._database_name = None

    def get_connection(self) -> Any:
        """
        TODO add description
        :return:
        """
        return self._connection

    def get_database_name(self) -> str:
        """
        TODO add description
        :return:
        """
        return self._database_name
