from gendiff.core.parse_data import parse_data


def get_diff(dict1, dict2):
    result = []
    merged_keys_list = list(dict1.keys())
    merged_keys_list.extend(list(dict2.keys()))
    merged_keys_list = list(set(merged_keys_list))
    merged_keys_list.sort()

    def get_values(_key):
        if not isinstance(dict1[_key], type(dict2[_key]))\
                or not isinstance(dict1[_key], dict):
            return {'old': dict1[_key], 'new': dict2[_key]}, []
        return {}, get_diff(dict1[_key], dict2[_key])

    for key in merged_keys_list:

        # get key status and values
        if key in dict1 and key not in dict2:
            key_status = 'disappear'
            values = {'only': dict1[key]}
            children = []
        elif key not in dict1 and key in dict2:
            key_status = 'appear'
            values = {'only': dict2[key]}
            children = []
        else:
            key_status = 'stay'
            values, children = get_values(key)
        result.append((key, {
            'key_status': key_status,
            'values': values,
            'children': children
        }))

    return result


def format_output_stylish(_diff_data):
    level = 0
    ind_str = '    '

    def get_string(_value, _level, _ind_str):
        if isinstance(_value, bool):
            return str(_value).lower()
        if _value is None:
            return 'null'
        if isinstance(_value, dict):
            result = '{\n'
            for key, value in _value.items():
                result += f'{_ind_str * (_level+1)}{key}: {get_string(value, _level+1, _ind_str)}\n'
            result += f'{_ind_str * _level}}}'
            return result
        return str(_value)

    def iteration(_diff_data, _level):
        _level += 1
        indent = ind_str * _level
        nonlocal result_string
        for key, meta in _diff_data:
            if not meta['children']:
                if meta['key_status'] == 'appear':
                    result_string += f"{indent[:-2]}+ {key}: {get_string(meta['values']['only'], _level, ind_str)}\n"
                if meta['key_status'] == 'disappear':
                    result_string += f"{indent[:-2]}- {key}: {get_string(meta['values']['only'], _level, ind_str)}\n"
                if meta['key_status'] == 'stay':
                    if meta['values']['old'] == meta['values']['new']:
                        result_string += f"{indent}{key}: {get_string(meta['values']['old'], _level, ind_str)}\n"
                    else:
                        result_string += f"{indent[:-2]}- {key}: {get_string(meta['values']['old'], _level, ind_str)}\n"
                        result_string += f"{indent[:-2]}+ {key}: {get_string(meta['values']['new'], _level, ind_str)}\n"
            else:
                if meta['key_status'] == 'appear':
                    result_string += f"{indent[:-2]}+ {key}: {{\n"
                if meta['key_status'] == 'disappear':
                    result_string += f"{indent[:-2]}- {key}: {{\n"
                if meta['key_status'] == 'stay':
                    result_string += f"{indent}{key}: {{\n"
                iteration(meta['children'], _level)
                result_string += f"{indent}}}\n"

    result_string = '{\n'
    iteration(_diff_data, level)
    result_string += '}\n'

    return result_string


def format_output(diff_data, _type='stylish'):
    if _type == 'stylish':
        return format_output_stylish(diff_data)


def generate_diff(file1_path, file2_path):
    file1_dict = parse_data(file1_path)
    file2_dict = parse_data(file2_path)
    diff_dict = get_diff(file1_dict, file2_dict)
    result = format_output(diff_dict)
    return result
