import pytest

def funct(a):
    return a+1

def test_all():
    assert funct(1)==2
