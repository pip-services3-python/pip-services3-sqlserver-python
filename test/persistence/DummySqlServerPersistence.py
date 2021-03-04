# -*- coding: utf-8 -*-
from pip_services3_commons.data import FilterParams

from pip_services3_sqlserver.persistence.IdentifiableSqlServerPersistence import IdentifiableSqlServerPersistence
from test.fixtures.IDummyPersistence import IDummyPersistence


class DummySqlServerPersistence(IdentifiableSqlServerPersistence, IDummyPersistence):
    def __init__(self):
        super(DummySqlServerPersistence, self).__init__('dummies')

    def _define_schema(self):
        self._clear_schema()
        self._ensure_schema(
            'CREATE TABLE [' + self._table_name + \
            '] ([id] VARCHAR(32) PRIMARY KEY, [key] VARCHAR(50), [content] VARCHAR(MAX))')
        self._ensure_index(self._table_name + '_key', {'key': 1}, {'unique': True})

    def get_page_by_filter(self, correlation_id, filter, paging, sort, select):
        filter = filter or FilterParams()
        key = filter.get_as_nullable_string('key')

        filter_condition = ''
        if key is not None:
            filter_condition += "[key]='" + key + "'"

        return super().get_page_by_filter(correlation_id, filter_condition, paging, None, None)

    def get_count_by_filter(self, correlation_id, filter):
        filter = filter or FilterParams()
        key = filter.get_as_nullable_string('key')

        filter_condition = ''
        if key is not None:
            filter_condition += "[key]='" + key + "'"

        return super().get_count_by_filter(correlation_id, filter_condition)
