import pytest
from tj.util.file.file_util import create_file_with_time, _create_dir_with_time

def funct(a):
    return a+1

def test_all():
    assert funct(1)==2

def test_file_util_funcs():
    root_path = 'test'
    filename = "test.md"
    final_dir = create_file_with_time(root_path, filename)
    temp_dir = _create_dir_with_time(root_path)
    assert final_dir.startswith(root_path+'/')
    assert final_dir.endswith('/'+filename)
