import unittest
import asyncio
import os
from dotenv import load_dotenv
from deepclient import DeepClient, DeepClientOptions
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class TestDeepClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        load_dotenv()
        transport = AIOHTTPTransport(
            url=os.getenv('URL_GQL'),
            headers={'Authorization': 'Bearer %s' % (os.getenv('BEARER_TOKEN'))}
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        self.options = DeepClientOptions(gql_client=client)
        self.client = DeepClient(self.options)

    def test_initialization(self):
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.client.client)

    async def test_methods_raise_not_implemented(self):
        async_methods = [
            'reserve', 'wait_for',
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
        new_record = {"type_id": 58, "from_id": 0, "to_id": 0}
        insert_result = await self.client.insert(new_record)
        insert_result_data = insert_result['data'][0]
        assert insert_result_data["type_id"] == new_record["type_id"]
        assert insert_result_data["from_id"] == new_record["from_id"]
        assert insert_result_data["to_id"] == new_record["to_id"]
        select_result = await self.client.select({"id": insert_result_data['id']})
        select_result_data = select_result['data'][0]
        assert select_result_data["type_id"] == new_record["type_id"]
        assert select_result_data["from_id"] == new_record["from_id"]
        assert select_result_data["to_id"] == new_record["to_id"]
        new_record2 = {"type_id": 59, "from_id": 0, "to_id": 0}
        record_list = [new_record, new_record2]
        insert_result = await self.client.insert(record_list)


    async def test_delete(self):
        new_record = {"type_id": 58, "from_id": 0, "to_id": 0}
        insert_result = await self.client.insert(new_record)
        insert_result_data = insert_result['data'][0]
        delete_result = await self.client.delete({"id": insert_result_data['id']})
        select_result = await self.client.select({"id": insert_result_data['id']})
        assert select_result['data'] == []

    async def test_update(self):
        new_record = {"type_id": 58, "from_id": 0, "to_id": 0}
        insert_result = await self.client.insert(new_record)
        insert_result_data = insert_result['data'][0]
        updated_record = {"type_id": 59, "from_id": 1, "to_id": 1}
        update_result = await self.client.update({"id": {"_eq": insert_result_data['id']}}, updated_record)
        select_result = await self.client.select({"id": {"_eq": insert_result_data['id']}})
        select_result_data = select_result['data'][0]
        assert select_result_data["type_id"] == updated_record["type_id"]
        assert select_result_data["from_id"] == updated_record["from_id"]
        assert select_result_data["to_id"] == updated_record["to_id"]

    async def test_serial_insert(self):
        typeTypeLinkId = await self.client.id("@deep-foundation/core", "Type")
        # One insert test
        linkIdsToDelete = []
        objects = {
            "type_id": 58, "from_id": 0, "to_id": 0
        }
        try:
            operation = {
                "table": 'links',
                "type": 'insert',
                "objects": objects
            }
            response = await self.client.serial({
                "operations": [
                    operation,
                ]
            })
            for link in response["data"]:
                linkIdsToDelete.append(link["id"])
                assert link["type_id"] == objects["type_id"]
                assert link["from_id"] == objects["from_id"]
                assert link["to_id"] == objects["to_id"]
        finally:
            for i in linkIdsToDelete:
                await self.client.delete({"id": i})

        # Multiple inserts in one operation test
        linkIdsToDelete = []
        try:
            result = await self.client.serial({
                "operations": [
                    operation,
                    operation
                ]
            })
            assert len(result["data"]) == 2
            for link in result["data"]:
                assert link
                linkIdsToDelete.append(link["id"])
        finally:
            for i in linkIdsToDelete:
                await self.client.delete({"id": i})

    async def test_serial_update(self):
        typeTypeLinkId = await self.client.id("@deep-foundation/core", "Type")

        # One update test
        linkIdsToDelete = []
        try:
            insert_result = await self.client.insert({
                "type_id": typeTypeLinkId,
                "string": {
                    "data": {
                        "value": "stringValue"
                    }
                }
            })

            newLinkId = insert_result["data"][0]["id"]
            updated_record = {"type_id": 59, "from_id": 1, "to_id": 1}

            linkIdsToDelete.append(newLinkId)
            operation = {
                "table": 'links',
                "type": 'update',
                "exp": {
                    "id": newLinkId,
                },
                "set": updated_record
            }

            updateResult = await self.client.serial({
                "operations": [operation]
            })
            self.assertEqual(len(updateResult["data"]), 1)
            for link in updateResult["data"]:
                self.assertEqual(link['type_id'], updated_record['type_id'])
                self.assertEqual(link["from_id"], updated_record["from_id"])
                self.assertEqual(link["to_id"], updated_record["to_id"])

        finally:
            for i in linkIdsToDelete:
                await self.client.delete({"id": i})
        # Two update test

        # One update test
        linkIdsToDelete = []
        try:
            insert_result_one = await self.client.insert({
                "type_id": typeTypeLinkId,
                "string": {
                    "data": {
                        "value": "stringValue"
                    }
                }
            })
            insert_result_two = await self.client.insert({
                "type_id": typeTypeLinkId,
                "string": {
                    "data": {
                        "value": "stringValue"
                    }
                }
            })
            newLinkId_one = insert_result_one["data"][0]["id"]
            newLinkId_two = insert_result_two["data"][0]["id"]
            updated_record = {"type_id": 59, "from_id": 1, "to_id": 1}

            linkIdsToDelete.append(newLinkId_one)
            linkIdsToDelete.append(newLinkId_two)
            operation_one = {
                "table": 'links',
                "type": 'update',
                "exp": {
                    "id": newLinkId_one,
                },
                "set": updated_record
            }
            operation_two = {
                "table": 'links',
                "type": 'update',
                "exp": {
                    "id": newLinkId_two,
                },
                "set": updated_record
            }

            updateResult = await self.client.serial({
                "operations": [operation_one, operation_two]
            })
            self.assertEqual(len(updateResult["data"]), 2)
            for link in updateResult["data"]:
                self.assertEqual(link['type_id'], updated_record['type_id'])
                self.assertEqual(link["from_id"], updated_record["from_id"])
                self.assertEqual(link["to_id"], updated_record["to_id"])

        finally:
            for i in linkIdsToDelete:
                await self.client.delete({"id": i})

    async def test_serial_delete(self):
        typeTypeLinkId = await self.client.id("@deep-foundation/core", "Type")

        # One delete test
        try:
            result = await self.client.insert({
                "type_id": typeTypeLinkId,
                "string": {
                    "data": {
                        "value": "stringValue"
                    }
                }
            })
            newLinkId = result["data"][0]["id"]

            operation = {
                "table": 'links',
                "type": 'delete',
                "exp": {
                    "id": newLinkId
                }
            }

            deleteResult = await self.client.serial({
                "operations": [operation]
            })
            self.assertEqual(len(deleteResult["data"]), 1)

            for link in result["data"]:
                self.assertEqual(link["id"], newLinkId)

            newLink = await self.client.select(newLinkId)
            newLinkData = newLink["data"]
            self.assertEqual(len(newLinkData), 0)
        except Exception:
            print("Error occurred")
        # Two delete test
        try:
            result_one = await self.client.insert({
                "type_id": typeTypeLinkId,
                "string": {
                    "data": {
                        "value": "stringValue"
                    }
                }
            })
            newLinkId_one = result_one["data"][0]["id"]
            result_two = await self.client.insert({
                "type_id": typeTypeLinkId,
                "string": {
                    "data": {
                        "value": "stringValue"
                    }
                }
            })
            newLinkId_two = result_two["data"][0]["id"]

            operation_one = {
                "table": 'links',
                "type": 'delete',
                "exp": {
                    "id": newLinkId_one
                }
            }
            operation_two = {
                "table": 'links',
                "type": 'delete',
                "exp": {
                    "id": newLinkId_two
                }
            }
            deleteResult = await self.client.serial({
                "operations": [operation_one, operation_two]
            })
            self.assertEqual(len(deleteResult["data"]), 2)

            self.assertEqual(deleteResult["data"]["id"][0], newLinkId_one)
            self.assertEqual(deleteResult["data"]["id"][1], newLinkId_two)

            newLink = await self.client.select(newLinkId_one)
            newLinkData = newLink["data"]
            self.assertEqual(len(newLinkData), 0)
            newLink = await self.client.select(newLinkId_two)
            newLinkData = newLink["data"]
            self.assertEqual(len(newLinkData), 0)
        except Exception:
            print("Error occurred")

    async def test_id(self):
        assert (await self.client.id("@deep-foundation/core", "Package")) == 2
        assert (await self.client.id("@deep-foundation/core", "Contain")) == 3
        assert (await self.client.id("@deep-foundation/core", "Value")) == 4


if __name__ == '__main__':
    unittest.main()
