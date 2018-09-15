#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import sys
from math import sqrt

import numpy as np

from joker.vizome.designer import ArrowDesigner

pi = np.pi

dataset1 = {
    'config': dict(alpha=pi / 4, beta=pi / 2, height1=1, height2=2),
    'lengths': [4],
    'awd_out': np.array([[
        [0, 0], [2, 2], [2, 1], [4, 1],
        [4, -1], [2, -1], [2, -2], [0, 0]
    ]])
}

dataset2 = {
    'config': dict(alpha=pi / 4, beta=pi / 3, height1=1, height2=2),
    'lengths': [2 - sqrt(3) / 2],
    'awd_out': np.array([[
        [0, 0], [2, 2],
        [2 - sqrt(3) / 2, 1. / 2], [2 - sqrt(3) / 2, 1. / 2],
        [2 - sqrt(3) / 2, -1. / 2], [2 - sqrt(3) / 2, -1. / 2],
        [2, -2], [0, 0]
    ]])
}

dataset3 = {
    'config': dict(alpha=pi / 4, beta=pi / 3, height1=1, height2=2),
    'lengths': [.6],
    'awd_out': np.array([[
        [0, 0], [2, 2], [.6, 0], [.6, 0],
        [.6, 0], [.6, 0], [2, -2], [0, 0]
    ]])
}


def arr_eq(arr1, arr2, precision=.001):
    res = np.abs(arr1 - arr2).reshape(-1).max() < precision
    if not res:
        print(arr1, file=sys.stderr)
        print(arr2, file=sys.stderr)
    return res


def test_amk():
    for ds in [dataset1, dataset2, dataset3]:
        arrow_designer = ArrowDesigner(**ds['config'])
        # result = calc.prototype(400).astype(np.int)
        awd_out = arrow_designer(ds['lengths'])
        assert arr_eq(awd_out, ds['awd_out'], .001)
        resultp = arrow_designer.prototype(ds['lengths'][0])
        assert arr_eq(resultp, ds['awd_out'][0], .001)
        # assert 1 == 2

        for x in np.arange(10, step=.01):
            if x == 0:
                continue
            resultp = arrow_designer.prototype(x)
            awd_out = arrow_designer([x])
            assert arr_eq(awd_out[0], resultp, .001)
            assert arr_eq(awd_out[:, 0, :], 0, .001)
            assert arr_eq(awd_out[:, 7, :], 0, .001)
            assert arr_eq(awd_out[:, 1, 1], ds['config']['height2'], .001)
            assert arr_eq(awd_out[:, 2, 1], awd_out[:, 3, 1])
            assert arr_eq(awd_out[:, 2, 1], -awd_out[:, 4, 1])
            assert arr_eq(awd_out[:, 2, 1], -awd_out[:, 5, 1])
            assert arr_eq(awd_out[:, 6, 1], -ds['config']['height2'])

        for i in range(100):
            x = np.random.randint(1, 1000)
            assert np.array_equal(
                arrow_designer([x]),
                arrow_designer([(x, 0)]),
            )


if __name__ == '__main__':
    test_amk()
