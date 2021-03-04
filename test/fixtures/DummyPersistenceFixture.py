# -*- coding: utf-8 -*-
from pip_services3_commons.data import AnyValueMap

from .Dummy import Dummy
from .IDummyPersistence import IDummyPersistence


class DummyPersistenceFixture:
    _dummy1 = Dummy(None, "Key 1", "Content 1")
    _dummy2 = Dummy(None, "Key 2", "Content 2")

    _persistence: IDummyPersistence = None

    def __init__(self, persistence):
        self._persistence = persistence

    def test_crud_operations(self):
        dummy1: Dummy
        dummy2: Dummy

        # Create one dummy
        dummy1 = self._persistence.create(None, self._dummy1)
        assert dummy1 is not None
        assert dummy1['id'] is not None
        assert dummy1['key'] == self._dummy1['key']
        assert dummy1['content'] == self._dummy1['content']

        # Create another dummy
        dummy2 = self._persistence.create(None, self._dummy2)
        assert dummy2 is not None
        assert dummy2['id'] is not None
        assert dummy2['key'] == self._dummy2['key']
        assert dummy2['content'] == self._dummy2['content']

        page = self._persistence.get_page_by_filter(None, None, None, None, None)
        assert page is not None
        assert len(page.data) == 2

        # Update the dummy
        dummy1['content'] = "Updated Content 1"
        result = self._persistence.update(None, dummy1)
        assert result is not None
        assert dummy1['id'] == result['id']
        assert dummy1['key'] == result['key']
        assert dummy1['content'] == result['content']

        # Set the dummy
        dummy1['content'] = "Updated Content 2"
        result = self._persistence.set(None, dummy1)
        assert result is not None
        assert dummy1['id'] == result['id']
        assert dummy1['key'] == result['key']
        assert dummy1['content'] == result['content']

        # Partially update the dummy
        result = self._persistence.update_partially(None, dummy1['id'], AnyValueMap.from_tuples(
            'content', 'Partially Updated Content 1'
        ))
        assert result is not None
        assert dummy1['id'] == result['id']
        assert dummy1['key'] == result['key']
        assert result['content'] == 'Partially Updated Content 1'

        # Get the dummy by Id
        result = self._persistence.get_one_by_id(None, dummy1['id'])
        # Try to get item
        assert result is not None
        assert dummy1['id'] == result['id']
        assert dummy1['key'] == result['key']

        # Delete the dummy
        result = self._persistence.delete_by_id(None, dummy1['id'])
        assert result is not None
        assert dummy1['id'] == result['id']
        assert dummy1['key'] == result['key']

        # Get the deleted dummy
        result = self._persistence.get_one_by_id(None, dummy1['id'])
        # Try to get item
        assert result is None

        # Get count dummies by filter
        count = self._persistence.get_count_by_filter(None, None)
        assert count == 1

    def test_batch_operations(self):
        dummy1: Dummy
        dummy2: Dummy

        # Create one dummy
        dummy1 = self._persistence.create(None, self._dummy1)
        assert dummy1 is not None
        assert dummy1['id'] is not None
        assert dummy1['key'] == self._dummy1['key']
        assert dummy1['content'] == self._dummy1['content']

        # Create another dummy
        dummy2 = self._persistence.create(None, self._dummy2)
        assert dummy2 is not None
        assert dummy2['id'] is not None
        assert dummy2['key'] == self._dummy2['key']
        assert dummy2['content'] == self._dummy2['content']

        # Read batch
        items = self._persistence.get_list_by_ids(None, [dummy1['id'], dummy2['id']])
        assert isinstance(items, list)
        assert len(items) == 2

        # Delete batch
        self._persistence.delete_by_ids(None, [dummy1['id'], dummy2['id']])

        # Read empty batch
        items = self._persistence.get_list_by_ids(None, [dummy1['id'], dummy2['id']])
        assert isinstance(items, list)
        assert len(items) == 0
