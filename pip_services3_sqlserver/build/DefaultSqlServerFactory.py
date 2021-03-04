# -*- coding: utf-8 -*-

from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from pip_services3_sqlserver.persistence.SqlServerConnection import SqlServerConnection


class DefaultSqlServerFactory(Factory):
    """
    Creates SqlServer components by their descriptors.

    See: :class:`SqlServerConnection <pip_services3_sqlserver.persistence.SqlServerConnection.SqlServerConnection>`,
    :class:`Factory <pip_services3_components.build.Factory.Factory>`
    """

    descriptor = Descriptor("pip-services", "factory", "sqlserver", "default", "1.0")
    sql_server_connection_descriptor = Descriptor("pip-services", "connection", "sqlserver", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultSqlServerFactory, self).__init__()
        self.register_as_type(
            DefaultSqlServerFactory.sql_server_connection_descriptor, sql_server_connection_descriptor)
