import os
import pytest
from gendiff.core.generate_diff import generate_diff


@pytest.fixture
def cwd():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def result(cwd):
    with open(f'{cwd}/../fixtures/test_generate_diff/result')as f:
        _result = f.read()
    return _result


@pytest.fixture
def result_tree(cwd):
    with open(f'{cwd}/../fixtures/test_generate_diff/result_tree')as f:
        _result = f.read()
    return _result


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
