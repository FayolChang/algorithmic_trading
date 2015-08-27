#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'phil.zhang'

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
from chapter15.data import HistoricCSVDataHandler
from chapter15 import event
import Queue

def test_data():
    events = Queue.Queue()
    headers = ['datetime','open', 'high', 'low', 'close', 'adj close']
    csv_handler = HistoricCSVDataHandler(events, '.', ['orcl'])
    csv_handler.update_bars()


if __name__ == '__main__':
    test_data()