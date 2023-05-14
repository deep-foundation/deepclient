import unittest
import asyncio
from deepclient import DeepClient, DeepClientOptions
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from deepclient.gql.mutation import insert_mutation, GenerateMutationOptions, generate_mutation
from deepclient.gql.serial import ISerialOptions, generate_serial, ISerialResult

class TestDeepClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        transport = AIOHTTPTransport(
            url='https://3006-deepfoundation-dev-12u849vgzrk.ws-eu97.gitpod.io/gql',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYWRtaW4iXSwieC1oYXN1cmEtZGVmYXVsdC1yb2xlIjoiYWRtaW4iLCJ4LWhhc3VyYS11c2VyLWlkIjoiMzc4In0sImlhdCI6MTY4MTMwNTA3OX0.Gr6wEG9VxMZ4mLqTEkZfN9kIYAjAXGm1r5YCXJTKRws'}
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
        assert self.client.serialize_where({"object": {"value": {"_contains": {"a": "b"}}}}) == {"object": {"value": {"_contains": {"a": "b"}}}}
        assert self.client.serialize_where({"value": "a"}) == {"string": {"value": {"_eq": "a"}}}
        assert self.client.serialize_where({ "from": { "type_id": 2, "value": "a" } }) == { "from": { "type_id": {"_eq": 2}, "string": {"value": {"_eq": "a"}} }}

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

        assert self.client.serialize_where({"_or": [{"type": ["@deep-foundation/core", "Value"]}, {"type": ["@deep-foundation/core", "User"]}]}) == {
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

        assert self.client.serialize_where({"type_id": {"_type_of": 25}}) == {"type": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
        assert self.client.serialize_where({"from_id": {"_type_of": 25}}) == {"from": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
        assert self.client.serialize_where({"to_id": {"_type_of": 25}}) == {"to": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}

    async def test_select(self):
        assert (await self.client.select(1))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8, 'value': None}
        assert (await self.client.select({ "id": 1 }))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8, 'value': None}
        assert (await self.client.select({ "id": { "_eq": 1 } }))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8, 'value': None}
    
    async def test_insert(self):
        result = await self.client.insert({ 'type_id': 1 })
        self.assertEqual(result.data[0].type_id, 1)
        select_result = await self.client.select({'id': result.data[0].id}) 
        self.assertEqual(select_result['data'], result.data[0].id)

    async def test_id(self):
        assert (await self.client.id("@deep-foundation/core", "Package")) == 2
        assert (await self.client.id("@deep-foundation/core", "Contain")) == 3
        assert (await self.client.id("@deep-foundation/core", "Value")) == 4

    def test_insert_mutation_without_options(self):
        table_name = "test_table"
        variables = {"column1": "value1", "column2": "value2"}
        options = GenerateMutationOptions(table_name=table_name, operation="insert", variables=variables)
        result = insert_mutation(table_name, variables, options)("some_alias", 0)

        assert result['tableName'] == "test_table"
        assert result['operation'] == "insert"
        assert result['variables'] == variables


    def test_insert_mutation_with_options(self):
        table_name = "test_table"
        variables = {"column1": "value1", "column2": "value2"}
        options = GenerateMutationOptions(table_name=table_name, operation="insert", variables=variables)
        result = insert_mutation(table_name, variables, options)("some_alias", 0)

        assert result['tableName'] == "test_table"
        assert result['operation'] == "insert"
        assert result['variables'] == variables
    


if __name__ == '__main__':
    unittest.main()
