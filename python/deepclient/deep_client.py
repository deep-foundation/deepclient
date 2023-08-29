import asyncio
import json
from typing import Any, Optional, Union, Dict, List
from .deep_client_options import DeepClientOptions
from .query import generate_query, generate_query_data
from .gql_operations.mutation import generate_mutation_data, generate_insert_mutation, generate_delete_mutation, \
    generate_update_mutation
from .gql_operations.serial import generate_serial

class DeepClient:
    _ids = {
      "@deep-foundation/core": {
        "Type": 1,
        "Package": 2,
        "Contain": 3,
        "Value": 4,
        "String": 5,
        "Number": 6,
        "Object": 7,
        "Any": 8,
        "Promise": 9,
        "Then": 10,
        "Resolved": 11,
        "Rejected": 12,
        "typeValue": 13,
        "packageValue": 14,
        "Selector": 15,
        "SelectorInclude": 16,
        "Rule": 17,
        "RuleSubject": 18,
        "RuleObject": 19,
        "RuleAction": 20,
        "containValue": 21,
        "User": 22,
        "Operation": 23,
        "operationValue": 24,
        "AllowInsert": 25,
        "AllowUpdate": 26,
        "AllowDelete": 27,
        "AllowSelect": 28,
        "File": 29,
        "SyncTextFile": 30,
        "syncTextFileValue": 31,
        "ExecutionProvider": 32,
        "JSExecutionProvider": 33,
        "TreeInclude": 34,
        "Handler": 35,
        "Tree": 36,
        "TreeIncludeDown": 37,
        "TreeIncludeUp": 38,
        "TreeIncludeNode": 39,
        "containTree": 40,
        "containTreeContain": 41,
        "containTreeAny": 42,
        "PackageNamespace": 43,
        "packageNamespaceValue": 44,
        "PackageActive": 45,
        "PackageVersion": 46,
        "packageVersionValue": 47,
        "HandleOperation": 48,
        "HandleInsert": 49,
        "HandleUpdate": 50,
        "HandleDelete": 51,
        "PromiseResult": 52,
        "promiseResultValueRelationTable": 53,
        "PromiseReason": 54,
        "Focus": 55,
        "focusValue": 56,
        "AsyncFile": 57,
        "Query": 58,
        "queryValue": 59,
        "Fixed": 60,
        "fixedValue": 61,
        "Space": 62,
        "spaceValue": 63,
        "AllowLogin": 64,
        "guests": 65,
        "Join": 66,
        "joinTree": 67,
        "joinTreeJoin": 68,
        "joinTreeAny": 69,
        "SelectorTree": 70,
        "AllowAdmin": 71,
        "SelectorExclude": 72,
        "SelectorFilter": 73,
        "HandleSchedule": 74,
        "Schedule": 75,
        "scheduleValue": 76,
        "Router": 77,
        "IsolationProvider": 78,
        "DockerIsolationProvider": 79,
        "dockerIsolationProviderValue": 80,
        "JSDockerIsolationProvider": 81,
        "Supports": 82,
        "dockerSupportsJs": 83,
        "PackageInstall": 84,
        "PackagePublish": 85,
        "packageInstallCode": 86,
        "packageInstallCodeHandler": 87,
        "packageInstallCodeHandleInsert": 88,
        "packagePublishCode": 89,
        "packagePublishCodeHandler": 90,
        "packagePublishCodeHandleInsert": 91,
        "Active": 92,
        "AllowPackageInstall": 93,
        "AllowPackagePublish": 94,
        "PromiseOut": 95,
        "promiseOutValue": 96,
        "PackageQuery": 97,
        "packageQueryValue": 98,
        "Port": 99,
        "portValue": 100,
        "HandlePort": 101,
        "PackageInstalled": 102,
        "PackagePublished": 103,
        "Route": 104,
        "RouterListening": 105,
        "RouterStringUse": 106,
        "routerStringUseValue": 107,
        "HandleRoute": 108,
        "routeTree": 109,
        "routeTreePort": 110,
        "routeTreeRouter": 111,
        "routeTreeRoute": 112,
        "routeTreeHandler": 113,
        "routeTreeRouterListening": 114,
        "routeTreeRouterStringUse": 115,
        "routeTreeHandleRoute": 116,
        "TreeIncludeIn": 117,
        "TreeIncludeOut": 118,
        "TreeIncludeFromCurrent": 119,
        "TreeIncludeToCurrent": 120,
        "TreeIncludeCurrentFrom": 121,
        "TreeIncludeCurrentTo": 122,
        "TreeIncludeFromCurrentTo": 123,
        "TreeIncludeToCurrentFrom": 124,
        "AllowInsertType": 125,
        "AllowUpdateType": 126,
        "AllowDeleteType": 127,
        "AllowSelectType": 128,
        "ruleTree": 129,
        "ruleTreeRule": 130,
        "ruleTreeRuleAction": 131,
        "ruleTreeRuleObject": 132,
        "ruleTreeRuleSubject": 133,
        "ruleTreeRuleSelector": 134,
        "ruleTreeRuleQuery": 135,
        "ruleTreeRuleSelectorInclude": 136,
        "ruleTreeRuleSelectorExclude": 137,
        "ruleTreeRuleSelectorFilter": 138,
        "Plv8IsolationProvider": 139,
        "JSminiExecutionProvider": 140,
        "plv8SupportsJs": 141,
        "Authorization": 142,
        "GeneratedFrom": 143,
        "ClientJSIsolationProvider": 144,
        "clientSupportsJs": 145,
        "Symbol": 146,
        "symbolValue": 147,
        "containTreeSymbol": 148,
        "containTreeThen": 149,
        "containTreeResolved": 150,
        "containTreeRejected": 151,
        "handlersTree": 152,
        "handlersTreeHandler": 153,
        "handlersTreeSupports": 154,
        "handlersTreeHandleOperation": 155,
        "HandleClient": 156,
        "HandlingError": 157,
        "handlingErrorValue": 158,
        "HandlingErrorReason": 159,
        "HandlingErrorLink": 160,
        "GqlEndpoint": 161,
        "MainGqlEndpoint": 162,
        "HandleGql": 163,
        "SupportsCompatable": 164,
        "plv8JSSupportsCompatableHandleInsert": 165,
        "plv8JSSupportsCompatableHandleUpdate": 166,
        "plv8JSSupportsCompatableHandleDelete": 167,
        "dockerJSSupportsCompatableHandleInsert": 168,
        "dockerJSSupportsCompatableHandleUpdate": 169,
        "dockerJSSupportsCompatableHandleDelete": 170,
        "dockerJSSupportsCompatableHandleSchedule": 171,
        "dockerJSSupportsCompatableHandlePort": 172,
        "dockerJSSupportsCompatableHandleRoute": 173,
        "clientJSSupportsCompatableHandleClient": 174,
        "promiseTree": 175,
        "promiseTreeAny": 176,
        "promiseTreeThen": 177,
        "promiseTreePromise": 178,
        "promiseTreeResolved": 179,
        "promiseTreeRejected": 180,
        "promiseTreePromiseResult": 181,
        "MigrationsEnd": 182
      }
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

    def path_to_where(self, start, *path):
        pckg = {"type_id": self._ids["@deep-foundation/core"]["Package"], "value": start} if isinstance(start, str) else {"id": start}
        where = pckg
        for item in path:
            if not isinstance(item, bool):
                nextWhere = {"in": {"type_id": self._ids["@deep-foundation/core"]["Contain"], "value": item, "from": where}}
                where = nextWhere
        return where

    def type_to_name(self, value_type):   
        if value_type is int:
            return 'number'
        if value_type is str:
            return 'string'

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
                        if key == 'value' or key == self.type_to_name(key_type):
                            setted = result[self.type_to_name(key_type)] = {'value': {'_eq': exp[key]}}
                        else:
                            setted = result[key] = {'_eq': exp[key]}
                    elif key not in self._boolExpFields and isinstance(exp[key], list):
                        setted = result[key] = self.serialize_where(self.path_to_where(*exp[key]))
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
                        self.path_to_where(exp[key]['_id'][0], *exp[key]['_id'][1:]), 'links'
                    )
                    if key == 'id':
                        result['_and'] = [*result.get('_and', []), _temp]
                    else:
                        result[key[:-3]] = _temp

                if not setted:
                    _temp = (
                        self.serialize_where(exp[key], env) if key in self._boolExpFields else (
                            self.serialize_where(exp[key], self._serialize.get(env, {}).get('relations', {}).get(key))
                        if self._serialize.get(env, {}).get('relations', {}).get(key) else exp[key]
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

    def __init__(self, options: Optional[DeepClientOptions] = None):
        if options is None:
            options = DeepClientOptions()

        self.__dict__.update(options.__dict__)
        self.client = self.gql_client if self.gql_client else None

    async def select(self, exp: Union[Dict, int, List[int]], options: Dict = {}) -> Dict:
        if not exp:
            return {"error": {"message": "!exp"}, "data": None, "loading": False, "networkStatus": None}

        if isinstance(exp, list):
            where = {"id": {"_in": exp}}
        elif isinstance(exp, dict):
            where = self.serialize_where(exp, options.get("table", "links"))
        else:
            where = {"id": {"_eq": exp}}
        
        table = options.get("table", self.table)
        returning = options.get("returning", self.default_returning(table))
        
        variables = options.get("variables", {})
        name = options.get("name", self.default_select_name)

        generated_query = generate_query({
            "queries": [
                generate_query_data({
                    "tableName": table,
                    "returning": returning,
                    "variables": {
                        "limit": where.get("limit", None),
                        **variables,
                        "where": where,
                    }
                }),
            ],
            "name": name,
        })
        
        q = await self.client.execute_async(generated_query['query'], variable_values=generated_query['variables'])
        data = q.get("q0", [])
        del q["q0"]
        return { **q, "data": data }

    def default_returning(self, table: str) -> str:
        if table == 'links':
            return self.links_select_returning
        elif table in ['strings', 'numbers', 'objects']:
            return self.values_select_returning
        elif table == 'selectors':
            return self.selectors_select_returning
        elif table == 'files':
            return self.files_select_returning
        else:
            return "id"

    async def insert(self, objects, options: Dict = {}) -> Dict:
        if not objects:
            return {"error": {"message": "!record"}, "data": None, "loading": False, "networkStatus": None}

        table = options.get("table", self.table)
        returning = options.get("returning", self.default_returning(table))
        name = options.get("name", 'insertLinks')

        generated_mutation = generate_insert_mutation({
            "mutations": [
                generate_mutation_data({
                    "tableName": table,
                    "returning": returning,
                    "variables": {
                        "input": objects,
                    },
                    "defs": ["$input: [links_insert_input!]!"]
                }),
            ],
            "name": name,
        })

        print(generated_mutation)
        m = await self.client.execute_async(generated_mutation['mutation'],
                                            variable_values=generated_mutation['variables'])
        data = m.get(table, [])
        del m[table]
        return {**m, "data": data['returning']}

    async def update(self, exp: Dict, value: Dict, options: Dict = {}) -> Dict:
        if not exp or not value:
            return {"error": {"message": "!exp or !value"}, "data": None, "loading": False,
                    "networkStatus": None}

        table = options.get("table", self.table)
        returning = options.get("returning", self.default_returning(table))
        name = options.get("name", "UPDATE")

        generated_mutation = generate_update_mutation({
            "mutations": [
                generate_mutation_data({
                    "tableName": table,
                    "returning": returning,
                    "variables": {
                        "set": value,
                        "where": exp,
                    }
                }),
            ],
            "name": name,
        })

        m = await self.client.execute_async(generated_mutation['mutation'],
                                            variable_values=generated_mutation['variables'])
        data = m.get("m0", [])
        # del m["m0"]
        return {**m, "data": data}

    async def delete(self, exp: Union[Dict, int, List[int]], options: Dict = {}) -> Dict:
        if not exp:
            raise ValueError('!exp')

        if isinstance(exp, list):
            where = {"id": {"_in": exp}}
        elif isinstance(exp, dict):
            where = self.serialize_where(exp, options.get("table", "links"))
        else:
            where = {"id": {"_eq": exp}}

        table = options.get("table", self.table)
        returning = options.get("returning", self.default_returning(table))

        variables = options.get("variables", {})
        name = options.get("name", 'delete')

        delete_mutation = generate_delete_mutation({
            'mutations': [
                generate_mutation_data({
                    'tableName': table,
                    'operation': 'delete',
                    'returning': returning,
                    'variables': {
                        **variables,
                        'where': where,
                    }
                }),
            ],
            'name': name,
        })

        try:
            m = await self.client.execute_async(delete_mutation['mutation'],
                                                variable_values=delete_mutation['variables'])
            data = m.get("object", [])
            # del m["object"]
            return {**m, "data": data}
        except Exception as e:
            # handle the exception, perhaps re-raise it after logging or cleaning up
            raise e

    async def serial(self, AsyncSerialParams: Dict):
        if not AsyncSerialParams:
            return {"error": {"message": "!AsyncSerialParams"}, "data": None, "loading": False, "networkStatus": None}
        if AsyncSerialParams["operations"]:
            operations = AsyncSerialParams["operations"]
        else:
            return {"error": {"message": "!operations"}, "data": None, "loading": False, "networkStatus": None}
        if AsyncSerialParams.get("returning"):
            returning = AsyncSerialParams["returning"]
        else:
            returning = "from_id id to_id type_id value"
        if AsyncSerialParams.get("silent"):
            silent = AsyncSerialParams["silent"]
        else:
            silent = False
        operations_grouped_by_type_and_table = {}

        for operation in operations:
            if operation["type"] not in operations_grouped_by_type_and_table:
                operations_grouped_by_type_and_table[operation["type"]] = {}

            if operation["table"] not in operations_grouped_by_type_and_table[operation["type"]]:
                operations_grouped_by_type_and_table[operation["type"]][operation["table"]] = []

            operations_grouped_by_type_and_table[operation["type"]][operation["table"]].append(operation)

        serial_actions = []

        for operation_type, operations_grouped_by_table in operations_grouped_by_type_and_table.items():
            for table, operations in operations_grouped_by_table.items():
                if operation_type == 'insert':
                    for operation in operations:
                        if AsyncSerialParams.get("name"):
                            name = AsyncSerialParams["name"]
                        else:
                            name = "insertLinks"
                        serial_actions.append(
                            generate_insert_mutation({
                                "mutations": [
                                    generate_mutation_data({
                                        "tableName": table,
                                        "returning": returning,
                                        "variables": {
                                            "input": operation["objects"],
                                        },
                                        "defs": ["$input: [links_insert_input!]!"]
                                    }),
                                ],
                                "name": name,
                            })
                        )
                elif operation_type == 'update':
                    for operation in operations:
                        if isinstance(operation["exp"], list):
                            where = {"id": {"_in": operation["exp"]}}
                        elif isinstance(operation["exp"], dict):
                            where = self.serialize_where(operation["exp"])
                        else:
                            where = {"id": {"_eq": operation["exp"]}}
                        if AsyncSerialParams.get("name"):
                            name = AsyncSerialParams["name"]
                        else:
                            name = "updateLinks"
                        serial_actions.append(
                            generate_update_mutation({
                                "mutations": [
                                    generate_mutation_data({
                                        "tableName": table,
                                        "returning": returning,
                                        "variables": {
                                            "set": operation["set"],
                                            "where": where,
                                        }
                                    }),
                                ],
                                "name": name,
                            })
                        )
                elif operation_type == 'delete':
                    for operation in operations:
                        if isinstance(operation["exp"], list):
                            where = {"id": {"_in": operation["exp"]}}
                        elif isinstance(operation["exp"], dict):
                            where = self.serialize_where(operation["exp"])
                        else:
                            where = {"id": {"_eq": operation["exp"]}}
                        if AsyncSerialParams.get("name"):
                            name = AsyncSerialParams["name"]
                        else:
                            name = "deleteLinks"
                        serial_actions.append(
                            generate_delete_mutation({
                                'mutations': [
                                    generate_mutation_data({
                                        'tableName': table,
                                        'operation': 'delete',
                                        'returning': returning,
                                        'variables': {
                                            'where': where,
                                        }
                                    }),
                                ],
                                'name': name,
                            })
                        )
        response = {"data": []}
        for action in serial_actions:
            try:
                response_part = await self.client.execute_async(
                    action["mutation"],
                    variable_values=action['variables'])
                response_part = response_part["links"]["returning"][0]
                response["data"].append(response_part)
            except Exception as e:
                if not silent:
                    raise e
                return {"error": str(e)}
        return response

    async def reserve(self):
        raise NotImplementedError("Method not implemented")

    async def wait_for(self):
        raise NotImplementedError("Method not implemented")

    # async def id(self, start: Union[DeepClientStartItem, BoolExpLink], *path: DeepClientPathItem) -> int:
    async def id(self, start: Any, *path: Any) -> int:
        if isinstance(start, dict):
            return (await self.select(start)).get("data")[0].get("id")
        
        if self._ids.get(start) and self._ids[start].get(path[0]):
            return self._ids[start][path[0]]
        
        q = await self.select(self.path_to_where(start, *path))
        if q.get("error"):
            raise Exception(q["error"])

        result = q.get("data")[0].get("id") or self._ids.get(start).get(path[0]) or 0
        if not result and path[-1] != True:
            raise Exception(f"Id not found by {json.dumps([start, *path])}")

        return result

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
