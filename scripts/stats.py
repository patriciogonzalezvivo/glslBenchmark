#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import csv
import numpy as np

def get_median_filtered(signal, threshold=3):
    """
    signal: is numpy array-like
    returns: signal, numpy array
    """
    difference = np.abs(signal - np.median(signal))
    median_difference = np.median(difference)
    s = 0 if median_difference == 0 else difference / float(median_difference)
    mask = s > threshold
    signal[mask] = np.median(signal)
    return signal