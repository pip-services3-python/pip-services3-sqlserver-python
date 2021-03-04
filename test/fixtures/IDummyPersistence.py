# -*- coding: utf-8 -*-
from abc import ABC
from typing import List, Union

from pip_services3_commons.data import FilterParams, PagingParams, AnyValueMap
from pip_services3_data import IGetter, IWriter, IPartialUpdater

from test.fixtures import Dummy


class IDummyPersistence(IGetter, IWriter, IPartialUpdater, ABC):

    def get_page_by_filter(self, correlation_id: Union[str, None], filter: Union[FilterParams, None],
                           paging: Union[PagingParams, None]):
        raise NotImplemented()

    def get_count_by_filter(self, correlation_id: Union[str, None], filter: Union[FilterParams, None]):
        raise NotImplemented()

    def get_list_by_ids(self, correlation_id: Union[str, None], ids: List[str]):
        raise NotImplemented()

    def get_one_by_id(self, correlation_id: Union[str, None], ids: List[str]):
        raise NotImplemented()

    def create(self, correlation_id: Union[str, None], item: Dummy):
        raise NotImplemented()

    def update(self, correlation_id: Union[str, None], item: Dummy):
        raise NotImplemented()

    def set(self, correlation_id: Union[str, None], item: Dummy):
        raise NotImplemented()

    def update_partially(self, correlation_id: Union[str, None], id: str, data: AnyValueMap):
        raise NotImplemented()

    def delete_by_id(self, correlation_id: Union[str, None], id: str):
        raise NotImplemented()

    def delete_by_ids(self, correlation_id: Union[str, None], ids: List[str]):
        raise NotImplemented()
