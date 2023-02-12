def format_value(value):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, (int, float)):
        return value
    return f"'{str(value)}'"


def get_values(meta):
    if meta['key_status'] == 'disappear':
        return ''
    if meta['key_status'] == 'appear':
        return f'{format_value(meta["values"]["only"])}'
    if meta['key_status'] == 'stay':
        return f'{format_value(meta["values"]["old"])} to {format_value(meta["values"]["new"])}'


def get_action(meta) -> str:
    actions = {
        'appear': 'was added with value: ',
        'disappear': 'was removed',
        'stay': 'was updated. From '
    }
    result_string = f'{actions[meta["key_status"]]}{get_values(meta)}'
    return result_string


def process_action(meta, prefix) -> str:
    if not meta['children']:
        return get_action(meta)
    return process_children(meta['children'], prefix)


def process_children(children, parent_acc='') -> str:
    out_string = ''
    for key, meta in children:
        prefix = f'{parent_acc}.{key}' if parent_acc else f'{key}'
        if meta['key_status'] == 'stay' and len(meta['values']) == 1:
            continue
        suffix = process_action(meta, prefix)
        if meta['children']:
            out_string += suffix
        else:
            out_string += f"Property '{prefix}' {suffix}\n"
    if parent_acc == '':
        out_string = out_string.rstrip()
    return out_string
