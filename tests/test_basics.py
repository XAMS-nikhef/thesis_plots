"""Basic tests and imports"""
import matplotlib.pyplot as plt
import thesis_plots
import numpy as np
from unittest import TestCase

def test_print_versions():
    thesis_plots.print_versions()
    thesis_plots.print_versions(['something_not_installed'])


class TestToStrTuple(TestCase):
    def test_to_str_tuple(self):
        tests = [
            'a',
            tuple(),
            ['a', 'b'],
            ('a', 'b'),
        ]
        for t in tests:
            res = thesis_plots.to_str_tuple(t)
            assert isinstance(res, tuple)
            if len(res):
                assert isinstance(res[0], str), res

    def test_bad_imput(self):
        with self.assertRaises(TypeError):
            thesis_plots.to_str_tuple(np.array(['a']))



def test_limit_setter():
    thesis_plots.LimitSetter()


def test_axhline():
    thesis_plots.labeled_hline(1,2,'3')
    thesis_plots.labeled_vline(1,2,'3')
    plt.clf()
