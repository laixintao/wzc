# -*- coding: utf-8 -*-
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from wzc.bootstrap import start_job

if __name__ == '__main__' and __package__ is None:
    start_job()