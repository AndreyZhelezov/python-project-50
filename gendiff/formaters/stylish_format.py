ind_str = '    '
minus_str = '- '
plus_str = '+ '


def get_keys(key, meta, level) -> list:
    prefix = ind_str * level
    minus_prefix = prefix[:-len(minus_str)] + minus_str
    plus_prefix = prefix[:-len(plus_str)] + plus_str
    if meta['key_status'] == 'disappear':
        return [f'{minus_prefix}{key}']
    if meta['key_status'] == 'appear':
        return [f'{plus_prefix}{key}']
    if meta['key_status'] == 'stay' and len(meta.get('values', 0)) == 2:
        return [f'{minus_prefix}{key}', f'{plus_prefix}{key}']
    return [f'{prefix}{key}']


def get_value_repr(value, level) -> str:
    if value == '':
        return ' '
    if isinstance(value, bool):
        return f' {str(value).lower()}'
    if value is None:
        return ' null'
    if isinstance(value, dict):
        result = ' {\n'
        for key, value in value.items():
            result += f'{ind_str * (level + 1)}{key}:' +\
                      f'{get_value_repr(value, level + 1)}\n'
        result += f'{ind_str * level}}}'
        return result
    return f' {str(value)}'


def get_values(meta, level) -> list:
    if meta.get('values'):
        return [get_value_repr(value, level + 1) + '\n' for _, value in meta['values'].items()]
    return [process_children(meta['children'], level + 1)]


def process_children(children, level) -> str:
    out_string = ' {\n' if level > 0 else '{\n'
    for key, meta in children:
        string_list = list(zip(get_keys(key, meta, level + 1), get_values(meta, level)))
        out_string += ''.join([f'{t[0]}:{t[1]}' for t in string_list])
    out_string += ind_str * level + '}' + ('\n' if level > 0 else '')
    return out_string
