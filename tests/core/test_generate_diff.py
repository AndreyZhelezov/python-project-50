import os
import pytest
from gendiff.core.generate_diff import generate_diff, get_diff, format_output


@pytest.fixture
def cwd():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def result(cwd):
    with open(f'{cwd}/../fixtures/test_generate_diff/result') as f:
        _result = f.read()
    return _result


@pytest.fixture
def result_tree(cwd):
    with open(f'{cwd}/../fixtures/test_generate_diff/result_tree') as f:
        _result = f.read()
    return _result


dict1 = {
    'common': {
        'setting1': 'Value 1',
        'setting2': 200,
        'setting3': True,
        'setting6': {
            'key': 'value',
            'doge': {
                'wow': ''
            }
        }
    },
    'group1': {
        'baz': 'bas',
        'foo': 'bar',
        'nest': {
            'key': 'value'
        }
    },
    'group2': {
        'abc': 12345,
        'deep': {
            'id': 45
        }
    }
}
dict2 = {
    'common': {
        'follow': False,
        'setting1': 'Value 1',
        'setting3': None,
        'setting4': 'blah blah',
        'setting5': {
            'key5': 'value5'
        },
        'setting6': {
            'key': 'value',
            'ops': 'vops',
            'doge': {
                'wow': 'so much'
            }
        }
    },
    'group1': {
        'foo': 'bar',
        'baz': 'bars',
        'nest': 'str'
    },
    'group3': {
        'deep': {
            'id': {
                'number': 45
            }
        },
        'fee': 100500
    }
}

expected_diff = [(
    'common', {
        'key_status': 'stay',
        'values': {},
        'children': [(
            'follow', {
                'key_status': 'appear',
                'values': {'only': False},
                'children': []}
        ), (
            'setting1', {
                'key_status': 'stay',
                'values': {'old': 'Value 1', 'new': 'Value 1'},
                'children': []}
        ), (
            'setting2', {
                'key_status': 'disappear',
                'values': {'only': 200},
                'children': []}
        ), (
            'setting3', {
                'key_status': 'stay',
                'values': {'old': True, 'new': None},
                'children': []}
        ), (
            'setting4', {
                'key_status': 'appear',
                'values': {'only': 'blah blah'},
                'children': []}
        ), (
            'setting5', {
                'key_status': 'appear',
                'values': {'only': {'key5': 'value5'}},
                'children': []}
        ), (
            'setting6', {
                'key_status': 'stay',
                'values': {},
                'children': [(
                    'doge', {
                        'key_status': 'stay',
                        'values': {},
                        'children': [(
                            'wow', {
                                'key_status': 'stay',
                                'values': {'old': '', 'new': 'so much'},
                                'children': []}
                        )]
                    }
                ), (
                    'key', {
                        'key_status': 'stay',
                        'values': {'old': 'value', 'new': 'value'},
                        'children': []}
                ), (
                    'ops', {
                        'key_status': 'appear',
                        'values': {'only': 'vops'},
                        'children': []}
                )]}
        )]}
), (
    'group1', {
        'key_status': 'stay',
        'values': {},
        'children': [(
            'baz', {
                'key_status': 'stay',
                'values': {'old': 'bas', 'new': 'bars'},
                'children': []}
        ), (
            'foo', {
                'key_status': 'stay',
                'values': {'old': 'bar', 'new': 'bar'},
                'children': []}
        ), (
            'nest', {
                'key_status': 'stay',
                'values': {'old': {'key': 'value'}, 'new': 'str'},
                'children': []}
        )]}
), (
    'group2', {
        'key_status': 'disappear',
        'values': {'only': {'abc': 12345, 'deep': {'id': 45}}},
        'children': []}
), (
    'group3', {
        'key_status': 'appear',
        'values': {'only': {'deep': {'id': {'number': 45}}, 'fee': 100500}},
        'children': []}
)]

output_stylish = """{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}
"""


def test_get_diff():
    assert get_diff(dict1, dict2) == expected_diff


def test_format_output():
    assert format_output(expected_diff) == output_stylish


def test_generate_diff(cwd, result):

    f1_path = f'{cwd}/../fixtures/test_generate_diff/file1.json'
    f2_path = f'{cwd}/../fixtures/test_generate_diff/file2.json'
    assert generate_diff(f1_path, f2_path) == result

    f1_path = f'{cwd}/../fixtures/test_generate_diff/file1.yaml'
    f2_path = f'{cwd}/../fixtures/test_generate_diff/file2.yaml'
    assert generate_diff(f1_path, f2_path) == result

    f1_path = f'{cwd}/../fixtures/test_generate_diff/file1.yml'
    f2_path = f'{cwd}/../fixtures/test_generate_diff/file2.yml'
    assert generate_diff(f1_path, f2_path) == result


def test_generate_diff_tree(cwd, result_tree):
    f1_path = f'{cwd}/../fixtures/test_generate_diff/file1_tree.json'
    f2_path = f'{cwd}/../fixtures/test_generate_diff/file2_tree.json'
    assert generate_diff(f1_path, f2_path) == result_tree

    f1_path = f'{cwd}/../fixtures/test_generate_diff/file1_tree.yaml'
    f2_path = f'{cwd}/../fixtures/test_generate_diff/file2_tree.yaml'
    assert generate_diff(f1_path, f2_path) == result_tree
