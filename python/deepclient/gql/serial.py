from typing import Any, Dict, List, Union


class ISerialOptions:
    actions: List[Any]
    name: str
    alias: str

    def __init__(self, actions=[], name='SERIAL', alias='m', **options: Dict[str, Any]):
        self.actions = actions
        self.name = name
        self.alias = alias
        self.options = options


class ISerialResult:
    mutation: Any
    mutation_string: str
    variables: Dict[str, Any]


def generate_serial(serial_options: ISerialOptions) -> ISerialResult:
    print('generateSerial',
          {'name': serial_options.name, 'alias': serial_options.alias, 'actions': serial_options.actions})
    called_actions = [action(serial_options.alias, i) if callable(action) else action for i, action in
                      enumerate(serial_options.actions)]
    defs = ','.join([','.join(m.get('defs', [])) for m in called_actions])
    mutation_string = (
            f"mutation {serial_options.name} ({defs}) " +
            ''.join([
                f"{m['resultAlias']}: {m['queryName']}({', '.join(m['args'])}) {{ {m['resultReturning']} }}"
                for m in called_actions
            ])
    )

    mutation = f"gql{mutation_string}"
    variables = {}
    for action in called_actions:
        for v, variable in action.get('resultVariables', {}).items():
            if v not in variables:
                variables[v] = variable

    result = ISerialResult()
    result.mutation = mutation
    result.mutation_string = mutation_string
    result.variables = variables
    result.options = serial_options.options

    print('generateSerialResult', {"mutation": mutation_string, "variables": variables})
    return result
