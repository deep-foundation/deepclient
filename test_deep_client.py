def test_serialize_where(deep_client):
    assert deep_client.serialize_where({"id": 5}) == {"id": {"_eq": 5}}
    assert deep_client.serialize_where({"id": {"_eq": 5}}) == {"id": {"_eq": 5}}
    assert deep_client.serialize_where({"value": 5}) == {"number": {"value": {"_eq": 5}}}
    assert deep_client.serialize_where({"value": "a"}) == {"string": {"value": {"_eq": "a"}}}
    assert deep_client.serialize_where({"number": 5}) == {"number": {"value": {"_eq": 5}}}
    assert deep_client.serialize_where({"string": "a"}) == {"string": {"value": {"_eq": "a"}}}
    assert deep_client.serialize_where({"number": {"value": {"_eq": 5}}}) == {"number": {"value": {"_eq": 5}}}
    assert deep_client.serialize_where({"string": {"value": {"_eq": "a"}}}) == {"string": {"value": {"_eq": "a"}}}
    assert deep_client.serialize_where({"object": {"value": {"_contains": {"a": "b"}}}}) == {"object": {"value": {"_contains": {"a": "b"}}}}

    # Note: Add `async` and `await` for the below test case when implementing in the actual test file
    type_id_contain = deep_client.id("@deep-foundation/core", "Contain")
    type_id_package = deep_client.id("@deep-foundation/core", "Package")
    assert deep_client.serialize_where(
        {
            "out": {
                "type_id": type_id_contain,
                "value": "b",
                "from": {
                    "type_id": type_id_package,
                    "value": "a",
                },
            },
        }
    ) == {
        "out": {
            "type_id": {"_eq": type_id_contain},
            "string": {"value": {"_eq": "b"}},
            "from": {
                "type_id": {"_eq": type_id_package},
                "string": {"value": {"_eq": "a"}},
            },
        }
    }

    assert deep_client.serialize_where({"value": 5, "link": {"type_id": 7}}, "value") == {
        "value": {"_eq": 5},
        "link": {
            "type_id": {"_eq": 7}
        },
    }

    assert deep_client.serialize_where({"type": ["@deep-foundation/core", "Value"]}) == {
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

    assert deep_client.serialize_where({"_or": [{"type": ["@deep-foundation/core", "Value"]}, {"type": ["@deep-foundation/core", "User"]}]}) == {
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

    id_value = deep_client.id("@deep-foundation/core", "Value")
    assert id_value == 4

    assert deep_client.serialize_where({"type_id": {"_type_of": 25}}) == {"type": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
    assert deep_client.serialize_where({"from_id": {"_type_of": 25}}) == {"from": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}
    assert deep_client.serialize_where({"to_id": {"_type_of": 25}}) == {"to": {"_by_item": {"path_item_id": {"_eq": 25}, "group_id": {"_eq": 0}}}}