from typing import Any, Dict, List, Optional, Tuple, Union

def generate_query_data(options: Dict[str, Any]) -> Any:
    def inner(alias: str, index: int) -> Dict[str, Any]:
        defs = []
        args = []
        for field in fields:
            defs.append(f"${field + index}: {field_types[field]}")
            args.append(f"{field}: ${field}{index}")

        result_alias = f"{alias}{index if isinstance(index, int) else ''}"
        result_variables = {}
        for v, variable in variables.items():
            result_variables[v + index] = variable

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