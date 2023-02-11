import gendiff.formaters.stylish_format as stylish_format
import gendiff.formaters.plain_format as plain_format
from gendiff.core.parse_data import parse_data


def get_diff(dict1, dict2):  # noqa: C901
    result = []
    merged_keys_list = list(dict1.keys())
    merged_keys_list.extend(list(dict2.keys()))
    merged_keys_list = list(set(merged_keys_list))
    merged_keys_list.sort()

    def get_stay_values(_key):
        if dict1[_key] == dict2[_key]:
            return {'equal': dict1[_key]}, []
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
            values, children = get_stay_values(key)
        result.append((key, {
            'key_status': key_status,
            'values': values,
            'children': children
        }))

    return result


def format_output(diff_data, _type):
    if _type == 'stylish':
        return stylish_format.process_children(diff_data, 0)
    if _type == 'plain':
        return plain_format.process_children(diff_data)


def generate_diff(file1_path, file2_path, _type):
    file1_dict = parse_data(file1_path)
    file2_dict = parse_data(file2_path)
    diff_dict = get_diff(file1_dict, file2_dict)
    result = format_output(diff_dict, _type)
    return result
