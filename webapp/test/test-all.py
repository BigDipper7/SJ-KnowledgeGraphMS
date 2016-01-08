#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from webapp.businesslogic.util.file.file_util import create_file_with_time, _create_dir_with_time
from webapp.businesslogic.util.import_util import _str_pre_process

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

    print "final_dir:{}".format(final_dir)
    print "temp_dir:{}".format(temp_dir)

def test_import_util():
    a = 'foofoofoo\nfoofoo'
    b = 'foofoofoo\\nfoofoo'
    g = _str_pre_process(a)
    assert b == g

    c = 'foo\n\nfooofoobar'
    d = 'foo\\n\\nfooofoobar'
    e,f = _str_pre_process(a,c)
    assert e==b and f==d
