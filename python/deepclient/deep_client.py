import asyncio
from typing import Any
from .deep_client_options import DeepClientOptions

class DeepClient:
    _ids = {
        "@deep-foundation/core": {},
    }

    _serialize = {
        "links": {
            "fields": {
                "id": "number",
                "from_id": "number",
                "to_id": "number",
                "type_id": "number",
            },
            "relations": {
                "from": "links",
                "to": "links",
                "type": "links",
                "in": "links",
                "out": "links",
                "typed": "links",
                "selected": "selector",
                "selectors": "selector",
                "value": "value",
                "string": "value",
                "number": "value",
                "object": "value",
                "can_rule": "can",
                "can_action": "can",
                "can_object": "can",
                "can_subject": "can",
                "down": "tree",
                "up": "tree",
                "tree": "tree",
                "root": "tree",
            },
        },
        "selector": {
            "fields": {
                "item_id": "number",
                "selector_id": "number",
                "query_id": "number",
                "selector_include_id": "number",
            },
            "relations": {
                "item": "links",
                "selector": "links",
                "query": "links",
            }
        },
        "can": {
            "fields": {
                "rule_id": "number",
                "action_id": "number",
                "object_id": "number",
                "subject_id": "number",
            },
            "relations": {
                "rule": "links",
                "action": "links",
                "object": "links",
                "subject": "links",
            }
        },
        "tree": {
            "fields": {
                "id": "number",
                "link_id": "number",
                "tree_id": "number",
                "root_id": "number",
                "parent_id": "number",
                "depth": "number",
                "position_id": "string",
            },
            "relations": {
                "link": "links",
                "tree": "links",
                "root": "links",
                "parent": "links",
                "by_link": "tree",
                "by_tree": "tree",
                "by_root": "tree",
                "by_parent": "tree",
                "by_position": "tree",
            }
        },
        "value": {
            "fields": {
                "id": "number",
                "link_id": "number",
                "value": "value",
            },
            "relations": {
                "link": "links",
            },
        },
    }

    _boolExpFields = {
        "_and": True,
        "_not": True,
        "_or": True,
    }

    def pathToWhere(self, start, *path):
        pckg = {"type_id": self._ids["@deep-foundation/core"]["Package"], "value": start} if isinstance(start, str) else {"id": start}
        where = pckg
        for item in path:
            if not isinstance(item, bool):
                nextWhere = {"in": {"type_id": self._ids["@deep-foundation/core"]["Contain"], "value": item, "from": where}}
                where = nextWhere
        return where

    def serialize_where(self, exp: Any, env: str = 'links') -> Any:
        if isinstance(exp, list):
            return [self.serialize_where(e, env) for e in exp]
        elif isinstance(exp, dict):
            keys = exp.keys()
            result = {}
            for key in keys:
                key_type = type(exp[key])
                setted = False
                is_id_field = key in ['type_id', 'from_id', 'to_id']
                if env == 'links':
                    if key_type in (str, int):
                        if key == 'value' or key == key_type.__name__:
                            setted = result[key_type.__name__] = {'value': {'_eq': exp[key]}}
                        else:
                            setted = result[key] = {'_eq': exp[key]}
                    elif key not in self._boolExpFields and isinstance(exp[key], list):
                        setted = result[key] = self.serialize_where(path_to_where(*exp[key]))
                elif env == 'value':
                    if key_type in (str, int):
                        setted = result[key] = {'_eq': exp[key]}

                ids = [
                    'rule_id', 'action_id', 'subject_id', 'object_id',
                    'link_id', 'tree_id', 'root_id', 'parent_id'
                ]
                if (
                    key_type == dict
                    and '_type_of' in exp[key]
                    and (
                        (env == 'links' and (is_id_field or key == 'id')) or
                        (env == 'selector' and key == 'item_id') or
                        (env == 'can' and key in ids) or
                        (env == 'tree' and key in ids) or
                        (env == 'value' and key == 'link_id')
                    )
                ):
                    _temp = setted = {
                        '_by_item': {
                            'path_item_id': {'_eq': exp[key]['_type_of']},
                            'group_id': {'_eq': 0}
                        }
                    }
                    if key == 'id':
                        result['_and'] = [*result.get('_and', []), _temp]
                    else:
                        result[key[:-3]] = _temp
                elif (
                    key_type == dict
                    and '_id' in exp[key]
                    and (
                        (env == 'links' and (is_id_field or key == 'id')) or
                        (env == 'selector' and key == 'item_id') or
                        (env == 'can' and key in ids) or
                        (env == 'tree' and key in ids) or
                        (env == 'value' and key == 'link_id')
                    )
                    and isinstance(exp[key]['_id'], list)
                    and len(exp[key]['_id']) >= 1
                ):
                    _temp = setted = self.serialize_where(
                        path_to_where(exp[key]['_id'][0], *exp[key]['_id'][1:]), 'links'
                    )
                    if key == 'id':
                        result['_and'] = [*result.get('_and', []), _temp]
                    else:
                        result[key[:-3]] = _temp

                if not setted:
                    _temp = (
                        self.serialize_where(exp[key], env) if key in self._boolExpFields else (
                            self.serialize_where(exp[key], _serialize.get(env, {}).get('relations', {}).get(key))
                        if _serialize.get(env, {}).get('relations', {}).get(key) else exp[key]
                    )
                )
                if key == '_and':
                    if '_and' in result:
                        result['_and'].extend(_temp)
                    else:
                        result['_and'] = _temp
                else:
                    result[key] = _temp
            return result
        else:
            if exp is None:
                raise ValueError('undefined in query')
            return exp

    def __init__(self, options: DeepClientOptions):
        self.gql_client = options.gql_client
        self.client = self.gql_client if self.gql_client else None

    async def select(self):
        raise NotImplementedError("Method not implemented")

    async def insert(self):
        raise NotImplementedError("Method not implemented")

    async def update(self):
        raise NotImplementedError("Method not implemented")

    async def delete(self):
        raise NotImplementedError("Method not implemented")

    async def serial(self):
        raise NotImplementedError("Method not implemented")

    async def reserve(self):
        raise NotImplementedError("Method not implemented")

    async def wait_for(self):
        raise NotImplementedError("Method not implemented")

    async def id(self):
        raise NotImplementedError("Method not implemented")

    def id_local(self):
        raise NotImplementedError("Method not implemented")

    async def guest(self):
        raise NotImplementedError("Method not implemented")

    async def jwt(self):
        raise NotImplementedError("Method not implemented")

    async def whoami(self):
        raise NotImplementedError("Method not implemented")

    async def login(self):
        raise NotImplementedError("Method not implemented")

    async def logout(self):
        raise NotImplementedError("Method not implemented")

    async def can(self):
        raise NotImplementedError("Method not implemented")

    async def name(self):
        raise NotImplementedError("Method not implemented")

    def name_local(self):
        raise NotImplementedError("Method not implemented")
