import unittest
import asyncio
from deepclient import DeepClient, DeepClientOptions
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class TestDeepClient(unittest.TestCase):

    def setUp(self):
        transport = AIOHTTPTransport(
            url='https://3006-deepfoundation-dev-kgyolopnp3g.ws-eu96b.gitpod.io/gql',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYWRtaW4iXSwieC1oYXN1cmEtZGVmYXVsdC1yb2xlIjoiYWRtaW4iLCJ4LWhhc3VyYS11c2VyLWlkIjoiMzc4In0sImlhdCI6MTY4MTMwNTA3OX0.Gr6wEG9VxMZ4mLqTEkZfN9kIYAjAXGm1r5YCXJTKRws'}
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        self.options = DeepClientOptions(gql_client=client)
        self.client = DeepClient(self.options)

    def test_initialization(self):
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.client.client)

    def test_methods_raise_not_implemented(self):
        async_methods = [
            'insert', 'update', 'delete', 'serial', 'reserve', 'wait_for',
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

        # # Note: Add `async` and `await` for the below test case when implementing in the actual test file
        # type_id_contain = self.client.id("@deep-foundation/core", "Contain")
        # type_id_package = self.client.id("@deep-foundation/core", "Package")

        assert self.client.serialize_where(
            {
                "out": {
                    "type_id": 3,
                    "value": "b",
                    "from": {
                        "type_id": 2,
                        "value": "a",
                    },
                },
            }
        ) == {
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

        # id_value = self.client.id("@deep-foundation/core", "Value")
        # assert id_value == 4

        assert self.client.serialize_where({"type_id": {"_type_of": 25}}) == {"type": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
        assert self.client.serialize_where({"from_id": {"_type_of": 25}}) == {"from": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
        assert self.client.serialize_where({"to_id": {"_type_of": 25}}) == {"to": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}

    def test_select(self):
        async def test_async_methods():
            assert (await self.client.select(1))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8, 'value': None}
            assert (await self.client.select({ "id": 1 }))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8, 'value': None}
            assert (await self.client.select({ "id": { "_eq": 1 }}))['data'][0] == {'id': 1, 'type_id': 1, 'from_id': 8, 'to_id': 8, 'value': None}

        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_async_methods())

    async def test_id_method(self):
        result = await self.client.id("@deep-foundation/core", "Contain")
        assert result == 3

if __name__ == '__main__':
    unittest.main()
