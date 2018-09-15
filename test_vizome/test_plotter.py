#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import random

import numpy as np
import pandas

from joker.vizome.designer import ArrowDesigner
from joker.vizome.plotter import ArrowPlotter


def test_prepare_polygon_data():
    arrow_maker = ArrowDesigner()
    for n in range(5):
        raw = arrow_maker(np.random.rand(n))
        pdata = list(ArrowPlotter.prepare_polygon_coordinates(raw))
        assert len(pdata) == n
        for s in pdata:
            assert s.count(',') == 8


def test_prepare_amk_input():
    df = pandas.DataFrame({
        'start': np.random.rand(5),
        'stop': np.random.rand(5),
        'fr': [random.choice('+-') for _ in range(5)],
    })
    data = ArrowPlotter.prepare_amk_input(df)
    for ix, fr in enumerate(df['fr']):
        if fr == '+':
            assert data[ix, 0] <= data[ix, 1]
        if fr == '-':
            assert data[ix, 0] >= data[ix, 1]


def test_prepare_plot_data():
    df = ArrowPlotter.read_csv('lwcexample.csv')
    print(df)
    for d in ArrowPlotter.prepare_plot_data(df):
        print(d)


if __name__ == '__main__':
    test_prepare_amk_input()
    test_prepare_polygon_data()
    test_prepare_plot_data()
