from typing import Any, Dict, List, Optional, Tuple, Union

def generate_query(options: Dict[str, Any]) -> Dict[str, Any]:
    queries = options.get("queries", [])
    operation = options.get("operation", "query")
    name = options.get("name", "QUERY")
    alias = options.get("alias", "q")

    called_queries = [query(alias, i) if callable(query) else query for i, query in enumerate(queries)]
    defs = ",".join([",".join(query["defs"]) for query in called_queries])
    queryString = f"{operation} {name} ({defs}) {{ {','.join([f'{query["resultAlias"]}: {query["queryName"]}({",".join(query["args"])}) {{ {query["resultReturning"]} }}' for query in called_queries])} }}"

    variables = {}
    for query in called_queries:
        for v, variable in query["resultVariables"].items():
            variables[v] = variable

    result = {
        "query": f"gql`{queryString}`",
        "variables": variables,
        "queryString": queryString,
    }
    return result
            "fields": fields,
            "fieldTypes": field_types,
            "index": index,
            "defs": defs,
            "args": args,
            "alias": alias,
            "resultAlias": result_alias,
            "resultVariables": result_variables,
        }

        return result

    table_name = options["tableName"]
    operation = options.get("operation", "query")
    query_name = options.get("queryName", table_name)
    returning = options.get("returning", "id")
    variables = options.get("variables", {})
    fields = ["distinct_on", "limit", "offset", "order_by", "where"]
    field_types = fields_inputs(table_name)

    return inner


def fields_inputs(table_name: str) -> Dict[str, str]:
    return {
        "distinct_on": f"[{table_name}_select_column!]",
        "limit": "Int",
        "offset": "Int",
        "order_by": f"[{table_name}_order_by!]",
        "where": f"{table_name}_bool_exp!",
    }