def inner(alias, index):
    def inner(alias, index):
        defs.append(f"${field + str(index)}: {field_types[field]}")
        return f"{alias}[{field}{str(index)}]"
    return f"{alias}[{field}{str(index)}]"