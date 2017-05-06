#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import random

import numpy as np
import pandas
from joker.vizome.arrowlib import ArrowMaker
from joker.vizome import prepare


def test_prepare_svg_polygon_data():
    maker = ArrowMaker()
    for n in range(5):
        raw = maker.calc(np.random.rand(n))
        pdata = list(prepare.prepare_svg_polygon_data(raw))
        assert len(pdata) == n
        for s in pdata:
            assert s.count(',') == 8


def test_prepare_arrow_maker_data():
    df = pandas.DataFrame({
        'start': np.random.rand(5),
        'stop': np.random.rand(5),
        'fr': [random.choice('+-') for _ in range(5)],
    })
    data = prepare.prepare_arrow_maker_data(df)
    for ix, fr in enumerate(df['fr']):
        if fr == '+':
            assert data[ix, 0] <= data[ix, 1]
        if fr == '-':
            assert data[ix, 0] >= data[ix, 1]


if __name__ == '__main__':
    test_prepare_arrow_maker_data()
    test_prepare_svg_polygon_data()
