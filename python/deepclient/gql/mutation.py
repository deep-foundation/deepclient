import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from gql import gql


def fields_inputs(fields: Dict[str, Any]) -> str:
    return ",".join([f'{k}:{v}' for k, v in fields.items()])


def generate_mutation_data(options: Dict[str, Any]) -> Dict[str, Any]:
    tableName = options.get("tableName", "")
    returning = options.get("returning", "")
    variables = options.get("variables", {})
    defs = options.get("defs", [])
    return {
        "resultAlias": tableName,
        "queryName": f"insert_{tableName}",
        "tableName": tableName,
        "returning": returning,
        "variables": variables,
        "defs": defs,
    }


def generate_insert_mutation(options: Dict[str, Union[str, List[Any]]]) -> Dict[str, Any]:
    mutations = options.get("mutations", [])
    operation = options.get("operation", "mutation")
    name = options.get("name", "INSERT")

    defs = ",".join([",".join(m.get("defs", [])) for m in mutations])
    mutation_bodies = [
        f'{m["resultAlias"]}: insert_{m["tableName"]}(objects: $input) {{ returning {{ {m["returning"]} }} }}' for m
        in mutations]
    mutation_string = f"{operation} {name}({defs}) {{{','.join(mutation_bodies)}}}"
    mutation = gql(mutation_string)

    result_variables = {}
    for m in mutations:
        for v, variable in m["variables"].items():
            result_variables[v] = variable

    return {
        "mutation": mutation,
        "variables": result_variables,
        "mutation_string": mutation_string,
    }


def generate_update_mutation(options: Dict[str, Union[str, List[Any]]]) -> Dict[str, Any]:
    mutations = options.get("mutations", [])
    operation = options.get("operation", "mutation")
    name = options.get("name", "UPDATE")

    defs = ",".join([",".join(m.get("defs", [])) for m in mutations])

    mutation_bodies = []
    for m in mutations:
        returning = "returning {" + f"{m['returning']}" + "}"
        mutation_body = f'{m["resultAlias"]}: update_{m["tableName"]}(where: $where, _set: $set) {{ affected_rows {returning}}}'
        mutation_bodies.append(mutation_body)

    mutation_string = f"{operation} {name}($where: links_bool_exp!, $set: links_set_input) {{{','.join(mutation_bodies)}}}"
    mutation = gql(mutation_string)

    result_variables = {}
    for m in mutations:
        for v, variable in m["variables"].items():
            result_variables[v] = variable

    return {
        "mutation": mutation,
        "variables": result_variables,
        "mutation_string": mutation_string,
    }


def generate_delete_mutation(options: Dict[str, Union[str, List[Any]]]) -> Dict[str, Any]:
    mutations = options.get("mutations", [])
    operation = options.get("operation", "mutation")
    name = options.get("name", "DELETE")

    called_mutations = [m("mutation", i) if callable(m) else m for i, m in enumerate(mutations)]
    defs = ",".join([",".join(m["defs"]) for m in called_mutations])

    mutation_bodies = []
    result_variables = {}
    variable_defs = []

    for m in called_mutations:
        returning = "returning {" + f"{m['returning']}" + "}"
        variable_name = f"{m['resultAlias']}Where"
        mutation_bodies.append(f'{m["resultAlias"]}: delete_{m["tableName"]}(where: ${variable_name}) {{affected_rows {returning}}}')
        variable_defs.append(f'${variable_name}: links_bool_exp!')  # replace with your actual type

        for v, variable in m["variables"].items():
            result_variables[variable_name] = variable

    mutation_string = f"{operation} {name}({','.join(variable_defs)}) {{{','.join(mutation_bodies)}}}"
    mutation = gql(mutation_string)

    return {
        "mutation": mutation,
        "variables": result_variables,
        "mutation_string": mutation_string,
    }

