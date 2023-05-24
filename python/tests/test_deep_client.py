import unittest
import asyncio
from deepclient import DeepClient, DeepClientOptions
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class TestDeepClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        transport = AIOHTTPTransport(
            url='https://3006-deepfoundation-dev-jbu8x3e7jwl.ws-eu97.gitpod.io/gql',
            headers={
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYWRtaW4iXSwieC1oYXN1cmEtZGVmYXVsdC1yb2xlIjoiYWRtaW4iLCJ4LWhhc3VyYS11c2VyLWlkIjoiMzc4In0sImlhdCI6MTY4MTMwNTA3OX0.Gr6wEG9VxMZ4mLqTEkZfN9kIYAjAXGm1r5YCXJTKRws'}
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        self.options = DeepClientOptions(gql_client=client)
        self.client = DeepClient(self.options)

    def test_initialization(self):
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.client.client)

    async def test_methods_raise_not_implemented(self):
        async_methods = [
            'insert', 'update', 'delete', 'serial', 'reserve', 'wait_for',
            'guest', 'jwt', 'whoami', 'login', 'logout', 'can', 'name'
        ]
        sync_methods = [
            'id_local', 'name_local'
        ]

        for method_name in async_methods:
            method = getattr(self.client, method_name)
            with self.assertRaises(NotImplementedError):
                await method()

        for method_name in sync_methods:
            method = getattr(self.client, method_name)
            with self.assertRaises(NotImplementedError):
                method()

    def test_serialize_where(self):
        assert self.client.serialize_where({"id": 5}) == {"id": {"_eq": 5}}
        assert self.client.serialize_where({"type_id": 5}) == {"type_id": {"_eq": 5}}
        assert self.client.serialize_where({"id": {"_eq": 5}}) == {"id": {"_eq": 5}}
        assert self.client.serialize_where({"value": 5}) == {"number": {"value": {"_eq": 5}}}
        assert self.client.serialize_where({"value": "a"}) == {"string": {"value": {"_eq": "a"}}}
        assert self.client.serialize_where({"number": 5}) == {"number": {"value": {"_eq": 5}}}
        assert self.client.serialize_where({"string": "a"}) == {"string": {"value": {"_eq": "a"}}}
        assert self.client.serialize_where({"number": {"value": {"_eq": 5}}}) == {"number": {"value": {"_eq": 5}}}
        assert self.client.serialize_where({"string": {"value": {"_eq": "a"}}}) == {"string": {"value": {"_eq": "a"}}}
        assert self.client.serialize_where({"object": {"value": {"_contains": {"a": "b"}}}}) == {
            "object": {"value": {"_contains": {"a": "b"}}}}
        assert self.client.serialize_where({"value": "a"}) == {"string": {"value": {"_eq": "a"}}}
        assert self.client.serialize_where({"from": {"type_id": 2, "value": "a"}}) == {
            "from": {"type_id": {"_eq": 2}, "string": {"value": {"_eq": "a"}}}}

        assert self.client.serialize_where({
            "out": {
                "type_id": 3,
                "value": "b",
                "from": {
                    "type_id": 2,
                    "value": "a",
                },
            },
        }) == {
                   "out": {
                       "type_id": {"_eq": 3},
                       "string": {"value": {"_eq": "b"}},
                       "from": {
                           "type_id": {"_eq": 2},
                           "string": {"value": {"_eq": "a"}},
                       },
                   }
               }

        assert self.client.serialize_where({"value": 5, "link": {"type_id": 7}}, "value") == {
            "value": {"_eq": 5},
            "link": {
                "type_id": {"_eq": 7}
            },
        }

        assert self.client.serialize_where({"type": ["@deep-foundation/core", "Value"]}) == {
            "type": {
                "in": {
                    "from": {
                        "string": {"value": {"_eq": "@deep-foundation/core"}},
                        "type_id": {"_eq": 2},
                    },
                    "string": {"value": {"_eq": "Value"}},
                    "type_id": {"_eq": 3},
                },
            },
        }

        assert self.client.serialize_where(
            {"_or": [{"type": ["@deep-foundation/core", "Value"]}, {"type": ["@deep-foundation/core", "User"]}]}) == {
                   "_or": [{
                       "type": {
                           "in": {
                               "from": {
                                   "string": {"value": {"_eq": "@deep-foundation/core"}},
                                   "type_id": {"_eq": 2},
                               },
                               "string": {"value": {"_eq": "Value"}},
                               "type_id": {"_eq": 3},
                           },
                       },
                   }, {
                       "type": {
                           "in": {
                               "from": {
                                   "string": {"value": {"_eq": "@deep-foundation/core"}},
                                   "type_id": {"_eq": 2},
                               },
                               "string": {"value": {"_eq": "User"}},
                               "type_id": {"_eq": 3},
                           },
                       },
                   }]
               }

        assert self.client.serialize_where({"type_id": {"_type_of": 25}}) == {
            "type": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
        assert self.client.serialize_where({"from_id": {"_type_of": 25}}) == {
            "from": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
        assert self.client.serialize_where({"to_id": {"_type_of": 25}}) == {
            "to": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}

    async def test_select(self):
        assert (await self.client.select(1))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8,
                                                            'value': None}
        assert (await self.client.select({"id": 1}))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8,
                                                                    'value': None}
        assert (await self.client.select({"id": {"_eq": 1}}))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8,
                                                                             'to_id': 8, 'value': None}

    async def test_insert(self):
        # Insert a new record
        new_record = {"type_id": 58, "from_id": 0, "to_id": 0}
        insert_result = await self.client.insert(new_record)
        insert_result_data = insert_result['data']['returning'][0]
        assert insert_result_data["type_id"] == new_record["type_id"]
        assert insert_result_data["from_id"] == new_record["from_id"]
        assert insert_result_data["to_id"] == new_record["to_id"]

        # Validate the insertion by selecting the inserted record
        select_result = await self.client.select({"id": insert_result_data['id']})
        select_result_data = select_result['data'][0]
        assert select_result_data["type_id"] == new_record["type_id"]
        assert select_result_data["from_id"] == new_record["from_id"]
        assert select_result_data["to_id"] == new_record["to_id"]

    async def test_delete(self):
        # Insert a new record
        new_record = {"type_id": 58, "from_id": 0, "to_id": 0}
        insert_result = await self.client.insert(new_record)
        insert_result_data = insert_result['data']['returning'][0]

        # Delete the record and assert it has been deleted
        delete_result = await self.client.delete({"id": insert_result_data['id']})

        # Now, try to select the deleted record. It should return an empty list.
        select_result = await self.client.select({"id": insert_result_data['id']})
        assert select_result['data'] == []
        # Add your assertion here to check if deletion was successful

        # # Insert multiple records to delete
        # new_record1 = {"type_id": 59, "from_id": 1, "to_id": 1}
        # new_record2 = {"type_id": 60, "from_id": 2, "to_id": 2}
        # insert_result1 = await self.client.insert(new_record1)
        # insert_result1_data = insert_result1['data']['returning'][0]
        # insert_result2 = await self.client.insert(new_record2)
        # insert_result2_data = insert_result2['data']['returning'][0]
        #
        # # Delete multiple records and assert they have been deleted
        # delete_result = await self.client.delete([insert_result1_data['id'], insert_result2_data['id']])
        # delete_result_data_ids = [result['id'] for result in delete_result['data']]
        # assert set(delete_result_data_ids) == {insert_result1_data['id'], insert_result2_data['id']}
        #
        # # Try to select the deleted records, expect an empty result for each
        # select_result1 = await self.client.select({"id": insert_result1_data['id']})
        # select_result2 = await self.client.select({"id": insert_result2_data['id']})
        # assert select_result1['data'] == []
        # assert select_result2['data'] == []

    async def test_update(self):
        # Insert a new record
        new_record = {"type_id": 58, "from_id": 0, "to_id": 0}
        insert_result = await self.client.insert(new_record)
        insert_result_data = insert_result['data']['returning'][0]

        # Update the inserted record
        updated_record = {"type_id": 59, "from_id": 1, "to_id": 1}
        update_result = await self.client.update({"id": {"_eq": insert_result_data['id']}}, updated_record)

        # Validate the update by selecting the updated record
        select_result = await self.client.select({"id": {"_eq": insert_result_data['id']}})
        select_result_data = select_result['data'][0]
        assert select_result_data["type_id"] == updated_record["type_id"]
        assert select_result_data["from_id"] == updated_record["from_id"]
        assert select_result_data["to_id"] == updated_record["to_id"]

    async def test_id(self):
        assert (await self.client.id("@deep-foundation/core", "Package")) == 2
        assert (await self.client.id("@deep-foundation/core", "Contain")) == 3
        assert (await self.client.id("@deep-foundation/core", "Value")) == 4


if __name__ == '__main__':
    unittest.main()
