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
    # a = 'foofoofoo\nfoofoo'
    # b = 'foofoofoo\\nfoofoo'
    # g = _str_pre_process(a)
    # assert b == g
    #
    # c = 'foo\n\nfooofoobar'
    # d = 'foo\\n\\nfooofoobar'
    # e,f = _str_pre_process(a,c)
    # assert e==b and f==d
    a = '  shdjsdh '
    b = 'shdjsdh'
    c = _str_pre_process(False, a)
    assert c == b

    e = '\n\n\n12nkasdui234\n \t'
    f = '12nkasdui234'
    g = _str_pre_process(False, e)
    assert g == f

    '''To be noticed: the following code snippet is to test flask.Markup.unescape func is good?
        but some how there is some error,
        - firstly, `unescape` method is use to unescape all html sensitive code such as '>' '&' to escape to '&nbsp;'
        such control characters, for security reasons.
        - and some how my method is wrong, assert is wrong, for NBSP(no-breaking space) is not space, so assert fails
        normally, so just to use such escape character to make it better, so in utf-8 string '\xc2\xa0' reperesent NBSP
        and in unicode NBSP is u'\xa0' , if it is escape in html, it is '&nbsp;'
    '''
    h = 'Lore&nbsp;m ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    i = 'Lore\xc2\xa0m ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    j = _str_pre_process(True, h)
    assert j == i
