def serialize_where(exp: any, env: str = 'links') -> any:
    def path_to_where(*args):
        pass  # Implement the path_to_where function

    if isinstance(exp, list):
        return [serialize_where(e, env) for e in exp]
    elif isinstance(exp, dict):
        keys = exp.keys()
        result = {}
        for key in keys:
            exp_key_type = type(exp[key])
            setted = False
            is_id_field = key in ['type_id', 'from_id', 'to_id']
            if env == 'links':
                if exp_key_type in {str, int}:
                    if key in {'value', type}:
                        setted = {type: {'value': {'_eq': exp[key]}}}
                    else:
                        setted = {key: {'_eq': exp[key]}}
                elif key not in _boolExpFields and isinstance(exp[key], list):
                    setted = {key: serialize_where(path_to_where(*exp[key]))}
            elif env == 'value':
                if exp_key_type in {str, int}:
                    setted = {key: {'_eq': exp[key]}}
    elif env == 'value':
        if exp_key_type in {str, int}:
            setted = {key: {'_eq': exp[key]}}
    if not setted:
        if key in _boolExpFields:
            _temp = serialize_where(exp[key], env)
            if key == '_and':
                if '_and' in result:
                    result['_and'].extend(_temp)
                else:
                    result['_and'] = _temp
            else:
                result[key] = _temp
        else:
            result[key] = exp[key]

    return result
    else:
        if exp is None:
            raise ValueError('undefined in query')
        return exp