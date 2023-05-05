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

    def serializeWhere(self, exp, env="links"):
        if isinstance(exp, list):
            return [self.serializeWhere(e, env) for e in exp]
        elif isinstance(exp, dict):
            result = {}
            for key, value in exp.items():
                setted = False
                is_id_field = key in ["type_id", "from_id", "to_id"]
                if env == "links":
                    if isinstance(value, (str, int)):
                        if key in ["value", str(value)]:
                            setted = result[value] = {"_eq": value}
                        else:
                            setted = result[key] = {"_eq": value}
                    elif key not in self._boolExpFields and isinstance(value, list):
                        setted = result[key] = self.pathToWhere(*value)
                elif env == "value":
                    if isinstance(value, (str, int)):
                        setted = result[key] = {"_eq": value}
                # ... (continue conversion)
            return result
        elif exp is None:
            raise ValueError("None in query")
        else:
            return exp