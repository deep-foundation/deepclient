import unittest
import asyncio
from deepclient import DeepClient, DeepClientOptions

class TestDeepClient(unittest.TestCase):

    def setUp(self):
        self.options = DeepClientOptions()
        self.client = DeepClient(self.options)

    def test_initialization(self):
        self.assertIsNotNone(self.client)
        self.assertIsNone(self.client.client)

    def test_methods_raise_not_implemented(self):
        async_methods = [
            'select', 'insert', 'update', 'delete', 'serial', 'reserve', 'wait_for',
            'id', 'guest', 'jwt', 'whoami', 'login', 'logout', 'can', 'name'
        ]
        sync_methods = [
            'id_local', 'name_local'
        ]

        async def test_async_methods():
            for method_name in async_methods:
                method = getattr(self.client, method_name)
                with self.assertRaises(NotImplementedError):
                    await method()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_async_methods())

        for method_name in sync_methods:
            method = getattr(self.client, method_name)
            with self.assertRaises(NotImplementedError):
                method()


    def test_serializeWhere(self):
        query = {
            "from_id": {"_type_of": "Package"},
            "_and": [
                {"to_id": {"_type_of": "Selector"}},
                {"type_id": {"_type_of": "Contain"}}
            ]
        }
        expected_result = {
            "from_id": {"_by_item": {"path_item_id": {"_eq": "Package"}, "group_id": {"_eq": 0}}},
            "_and": [
                {"to_id": {"_by_item": {"path_item_id": {"_eq": "Selector"}, "group_id": {"_eq": 0}}}},
                {"type_id": {"_by_item": {"path_item_id": {"_eq": "Contain"}, "group_id": {"_eq": 0}}}}
            ]
        }
        serialized_query = self.client.serialize_where(query)
        self.assertEqual(serialized_query, expected_result)


if __name__ == '__main__':
    unittest.main()
