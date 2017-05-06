#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import numpy
import pandas


def parse_strand(s):
    try:
        return int(s)
    except ValueError:
        return {'+': 1, '-': -1}[s]


def read_csv(p):
    return pandas.read_csv(p, sep=None, engine='python')


def prepare_arrow_maker_data(dframe):
    arr = dframe[['start', 'stop']].values
    arr_min = arr.min(axis=1, keepdims=True)
    arr_max = arr.max(axis=1, keepdims=True)
    arr_orient = dframe['fr'].values != '-'
    arr_orient.dtype = 'uint8'
    heads = arr_min * arr_orient + arr_max * (1 - arr_orient)
    tails = arr_max * arr_orient + arr_min * (1 - arr_orient)
    heads.shape = -1, 1
    tails.shape = -1, 1
    return numpy.concatenate([heads, tails], axis=1)


def prepare_svg_polygon_data(raw):
    """
    :param raw: 3d array returned by ArrowMaker.calc(..)
    :return: 
    """
    for arrow in raw:
        yield ' '.join('{},{}'.format(x, y) for (x, y) in arrow)
