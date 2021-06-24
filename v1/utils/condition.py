def get_condition(filters: str):
    position = filters.find("[")
    key = filters[:position]
    filters = filters[position + 1:]
    position = filters.find("]")
    condition = filters[:position]
    value = filters[position + 1:]

    return {
        "key": key,
        "condition": condition,
        "value": value,
    }
