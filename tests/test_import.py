# content of test_sample.py
# add the parent subfolder to path
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from train import *  # noqa: F403


def test_import():
    # import were done before if needs be
    assert 4 == 4


def test_model():
    pass 
