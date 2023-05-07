from typing import Any, Dict, List, Optional, Tuple, Union
from gql import gql

def generate_query_data(options: Dict[str, Any]) -> Any:
    def inner(alias: str, index: int) -> Dict[str, Any]:
        defs = []
        args = []
        for field in fields:
            defs.append(f"${field + str(index)}: {field_types[field]}")
            args.append(f"{field}: ${field}{index}")

        result_alias = f"{alias}{index if isinstance(index, int) else ''}"
        result_variables = {}
        for v, variable in variables.items():
            result_variables[v + str(index)] = variable

        result = {
            "tableName": table_name,
            "operation": operation,
            "queryName": query_name,
            "returning": returning,
            "variables": variables,
            "resultReturning": returning,
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

def generate_query(options: Dict[str, Union[str, List[Any]]]) -> Dict[str, Any]:
    queries = options.get("queries", [])
    operation = options.get("operation", "query")
    name = options.get("name", "QUERY")
    alias = options.get("alias", "q")

    called_queries = [m(alias, i) if callable(m) else m for i, m in enumerate(queries)]
    defs = ",".join([",".join(m["defs"]) for m in called_queries])
    query_body = ','.join([f'{m["resultAlias"]}: {m["queryName"]}({",".join(m["args"])}) {{ {m["resultReturning"]} }}' for m in called_queries])
    query_string = f"{operation} {name} ({defs}) {{{query_body}}}"
    query = gql(query_string)

    variables = {}
    for action in called_queries:
        for v, variable in action["resultVariables"].items():
            variables[v] = variable

    # print(query_string)
    # print(variables)
    result = {
        "query": query,
        "variables": variables,
        "query_string": query_string,
    }
    return result