import os
import pytest
from gendiff.core.generate_diff import generate_diff


@pytest.fixture
def cwd():
    return os.path.dirname(os.path.realpath(__file__))


def test_generate_diff(cwd):
    print(__file__)
    with open(f'{cwd}/../fixtures/test_generate_diff/result')as f:
        result = f.read()
    f1_path = f'{cwd}/../fixtures/test_generate_diff/file1.json'
    f2_path = f'{cwd}/../fixtures/test_generate_diff/file2.json'
    assert generate_diff(f1_path, f2_path) == result
