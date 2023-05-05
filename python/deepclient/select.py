# select.py

from typing import Any, Dict, List, Union

class Select:

    def __init__(self):
        pass

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
        
        variables = options.get("variables", None)
        name = options.get("name", self.default_select_name)
        
        q = await self.client.query(self.generate_query({
            "queries": [
                self.generate_query_data({
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
        }))

        return {**q, "data": q.get("data", {}).get("q0", None)}

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