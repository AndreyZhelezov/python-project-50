from gendiff.core.parse_data import parse_data


def generate_diff(file1_path, file2_path):
    file1_dict = parse_data(file1_path)
    file2_dict = parse_data(file2_path)
    keys_list = list(set(list(file1_dict.keys()) + list(file2_dict.keys())))
    keys_list.sort()

    result_string = '{\n'
    indent = '  '
    for key in keys_list:
        key1 = key2 = key
        val1 = file1_dict.pop(key1, None)
        val1 = str(val1).lower() if isinstance(val1, bool) else val1
        val2 = file2_dict.pop(key2, None)
        val2 = str(val2).lower() if isinstance(val2, bool) else val2
        if val1 is None:
            result_string += f'{indent}+ {key2}: {val2}\n'
            continue
        if val2 is None:
            result_string += f'{indent}- {key1}: {val1}\n'
            continue
        if val1 != val2:
            result_string += f'{indent}- {key1}: {val1}\n'
            result_string += f'{indent}+ {key2}: {val2}\n'
            continue
        result_string += f'{indent}  {key1}: {val1}\n'
    result_string += '}\n'
    return result_string
