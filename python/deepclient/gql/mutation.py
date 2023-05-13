import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


def fields_inputs(table_name: str) -> Dict[str, str]:
    return {
        "distinct_on": f"[{table_name}_select_column!]",
        "limit": "Int",
        "offset": "Int",
        "order_by": f"[{table_name}_order_by!]",
        "where": f"{table_name}_bool_exp!",
        "objects": f"[{table_name}_insert_input!]!",
        "object": f"{table_name}_insert_input!",
        "_inc": f"{table_name}_inc_input",
        "_set": f"{table_name}_set_input",
        "on_conflict": f"{table_name}_on_conflict",
    }


class GenerateMutationOptions:
    def __init__(
            self,
            table_name: str,
            operation: str,
            query_name: Optional[str] = None,
            returning: Optional[str] = None,
            variables: Optional[Dict[str, Any]] = None,
    ):
        self.table_name = table_name
        self.operation = operation
        self.query_name = query_name or f"{operation}_{table_name}"
        self.returning = returning or "id"
        self.variables = variables or {}


class GenerateMutationResult(GenerateMutationOptions):
    def __init__(
            self,
            result_returning: str,
            fields: List[str],
            field_types: Dict[str, str],
            defs: List[str],
            args: List[str],
            alias: str,
            index: int,
            result_alias: str,
            result_variables: Dict[str, Any],
            *args_: List[Any],
            **kwargs_: Dict[str, Any],
    ):
        super().__init__(*args_, **kwargs_)
        self.result_returning = result_returning
        self.fields = fields
        self.field_types = field_types
        self.defs = defs
        self.args = args
        self.alias = alias
        self.index = index
        self.result_alias = result_alias
        self.result_variables = result_variables


def generate_mutation(tableName: str, operation: str, queryName: str = None, returning: str = 'id',
                      variables: dict = None):

    if queryName is None:
        queryName = f"{operation}_{tableName}"

    if variables is None:
        variables = {}

    fields = {
        'insert': ['objects', 'on_conflict'],
        'update': ['_inc', '_set', 'where'],
        'delete': ['where']
    }.get(operation, [])

    fieldTypes = fields_inputs(tableName)

    def builder(alias: str, index: int):

        defs = []
        args = []

        for field in fields:
            if field in variables:
                defs.append(f"${field}{index}: {fieldTypes[field]}")
                args.append(f"{field}: ${field}{index}")

        result_alias = f"{alias}{index if isinstance(index, int) else ''}"
        result_returning = f"returning {{ {returning} }}"
        result_variables = {f"{v}{index}": variable for v, variable in variables.items()}

        result = {
            "tableName": tableName,
            "operation": operation,
            "queryName": queryName,
            "returning": returning,
            "variables": variables,
            "resultReturning": result_returning,
            "fields": fields,
            "fieldTypes": fieldTypes,
            "index": index,
            "defs": defs,
            "args": args,
            "alias": alias,
            "resultAlias": result_alias,
            "resultVariables": result_variables,
        }
        return result

    return builder


def insert_mutation(table_name: str, variables: Dict[str, Any], options: Optional[GenerateMutationOptions] = None) -> \
        Callable[[str, int], GenerateMutationResult]:
    if options is None:
        options = GenerateMutationOptions(table_name=table_name, operation="insert", variables=variables)
    else:
        options.table_name = table_name
        options.operation = "insert"
        options.variables = variables
        return generate_mutation(options)


def update_mutation(table_name: str, variables: Dict[str, Any], options: Optional[GenerateMutationOptions] = None) -> \
        Callable[[str, int], GenerateMutationResult]:
    if options is None:
        options = GenerateMutationOptions(table_name=table_name, operation="update", variables=variables)
    else:
        options.table_name = table_name
        options.operation = "update"
        options.variables = variables
        return generate_mutation(options)


def delete_mutation(table_name: str, variables: Dict[str, Any], options: Optional[GenerateMutationOptions] = None) -> \
        Callable[[str, int], GenerateMutationResult]:
    if options is None:
        options = GenerateMutationOptions(table_name=table_name, operation="delete", variables=variables)
    else:
        options.table_name = table_name
        options.operation = "delete"
        options.variables = variables
        return generate_mutation(options)
