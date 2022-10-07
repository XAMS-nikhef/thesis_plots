"""Basic tests and imports"""
import numpy as np
import pandas as pd

import thesis_plots


def test_print_versions():
    thesis_plots.print_versions()


def test_to_str_tuple():
    tests = [
        'a',
        tuple(),
        ['a', 'b'],
        ('a', 'b'),
        np.array(['a', 'b']),
        pd.Series(['a', 'b'])
    ]
    for t in tests:
        res = thesis_plots.to_str_tuple(t)
        assert isinstance(res, tuple)
        if len(res):
            assert isinstance(res[0], str), res
