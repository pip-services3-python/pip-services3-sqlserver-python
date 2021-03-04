# -*- coding: utf-8 -*-
import json

from pip_services3_commons.data import IIdentifiable

from pip_services3_sqlserver.persistence.IdentifiableSqlServerPersistence import IdentifiableSqlServerPersistence


class IdentifiableJsonSqlServerPersistence(IdentifiableSqlServerPersistence, IIdentifiable):
    """
    Abstract persistence component that stores data in SqlServer in JSON or JSONB fields
    and implements a number of CRUD operations over data items with unique ids.
    The data items must implement :class:`IIdentifiable <pip_services3_commons.data.IIdentifiable.IIdentifiable>` interface.

    The JSON table has only two fields: id and data.

    In basic scenarios child classes shall only override :func:`get_page_by_filter <pip_services3_sqlserver.persistence.IdentifiableJsonSqlServerPersistence.get_page_by_filter>`,
    :func:`get_list_by_filter <pip_services3_sqlserver.persistence.IdentifiableJsonSqlServerPersistence.get_list_by_filter>` or :func:`delete_by_filter <pip_services3_sqlserver.persistence.IdentifiableJsonSqlServerPersistence.delete_by_filter>`
    operations with specific filter function.
    All other operations can be used out of the box.

    In complex scenarios child classes can implement additional operations by
    accessing **self._collection** and **self._model** properties.

    ### Configuration parameters ###
        - collection:                  (optional) SqlServer collection name
        - connection(s):
            - discovery_key:             (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`
            - host:                      host name or IP address
            - port:                      port number (default: 27017)
            - uri:                       resource URI or connection string with all parameters in it
        - credential(s):
            - store_key:                 (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>`
            - username:                  (optional) user name
            - password:                  (optional) user password
        - options:
            - connect_timeout:      (optional) number of milliseconds to wait before timing out when connecting a new client (default: 0)
            - idle_timeout:         (optional) number of milliseconds a client must sit idle in the pool and not be checked out (default: 10000)
            - max_pool_size:        (optional) maximum number of clients the pool should contain (default: 10)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages components to pass log messages
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` services
        - `*:credential-store:*:*:1.0` (optional) :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>` stores to resolve credentials

    Example:

    .. code-block:: python
    
        class MySqlServerPersistence(IdentifiableJsonSqlServerPersistence):
            def __init__(self):
                super(MySqlServerPersistence, self).__init__("mydata", MyDataSqlServerSchema())

            def __compose_filter(self, filter):
                filter = filter or FilterParams()
                criteria = []
                name = filter.get_as_nullable_string('name')
                if name:
                    criteria.append({'name': name})
                return {'$and': criteria} if len(criteria) > 0 else None

            def get_page_by_filter(self, correlation_id, filter, paging):
                return super().get_page_by_filter(correlation_id, self.__compose_filter(filter), paging, None, None)

        persistence = MySqlServerPersistence()
        persistence.configure(ConfigParams.from_tuples(
            "host", "localhost",
            "port", 27017
        ))

        persistence.open('123')
        persistence.create('123', {'id': "1", 'name': "ABC"})
        page = persistence.get_page_by_filter('123', FilterParams.from_tuples('name', 'ABC'), None)
        print(page.data) # Result: { id: "1", name: "ABC" }

        persistence.delete_by_id("123", "1")
        # ...
    """

    def __init__(self, table_name):
        """
        Creates a new instance of the persistence component.
        """
        super(IdentifiableJsonSqlServerPersistence, self).__init__(table_name)

    def _ensure_table(self, id_type='VARCHAR(32)', data_type='NVARCHAR(MAX)'):
        """
        Adds DML statement to automatically create JSON(B) table

        :param id_type: type of the id column (default: TEXT)
        :param data_type: type of the data column (default: JSONB)
        """
        query = "CREATE TABLE " + self._quote_identifier(
            self._table_name) + " ([id] " + id_type + " PRIMARY KEY, [data] " + data_type + ")"
        self._auto_create_object(query)

    def _convert_to_public(self, value):
        """
        Converts object value from internal to public format.

        :param value:  an object in internal format to convert.
        :return: converted object in public format.
        """
        if value is None:
            return None
        return json.loads(value.data)

    def _convert_from_public(self, value):
        """
        Convert object value from public to internal format.

        :param value: an object in public format to convert.
        :return: converted object in internal format.
        """
        if value is None:
            return None

        result = {
            'id': value['id'],
            'data': json.dumps(dict(value))
        }

        return result

    def _convert_from_public_partial(self, value):
        """
        Converts the given object from the public partial format.

        :param value: the object to convert from the public partial format.
        :return: the initial object.
        """
        return dict(value)

    def update_partially(self, correlation_id, id, data):
        """
        Updates only few selected fields in a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param id: an id of data item to be updated.
        :param data: a map with fields to be updated.
        :return: updated item or raise error
        """
        if data is None or id is None:
            return

        row = self._convert_from_public_partial(data.get_as_object())
        columns = list(row.keys())
        values = list(row.values())

        set = "[data]"
        for column in columns:
            set = "JSON_MODIFY(" + set + ",'$." + column + "',?)"

        values.append(id)

        query = "UPDATE " + self._quote_identifier(
            self._table_name) + " SET [data]=" + set + " OUTPUT INSERTED.* WHERE [id]=?"

        result = self._request(query, values)

        self._logger.trace(correlation_id, "Updated partially in %s with id = %s", self._table_name, id)

        new_item = self._convert_to_public(result[0]) if result and result[0] and len(result) == 1 else None

        return new_item
