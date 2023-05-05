import unittest
from deep_client import DeepClient


class TestDeepClient(unittest.TestCase):

    def setUp(self):
        self.dc = DeepClient()

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
        serialized_query = self.dc.serializeWhere(query)
        self.assertEqual(serialized_query, expected_result)


if __name__ == '__main__':
    unittest.main()