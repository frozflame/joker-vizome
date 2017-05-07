#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import numpy
import pandas
from joker.vizome.designer import ArrowDesigner
from lxml.builder import E
from lxml.etree import tostring

default_polygon_style = {
    'stroke-width': 1,
    'fill-opacity': 0.7,
    'stroke': 'black',
    'stroke-opacity': 0.8,
}

default_text_style = {
    'font-size': 14,
    'font-family': 'Times New Roman',
}


class ArrowPlotter(object):
    def __init__(self, text_angle=45, text_style=None, polygon_style=None):
        self.text_angle = text_angle
        self.text_style = default_text_style
        self.polygon_style = dict(default_polygon_style)
        if text_style:
            self.text_style.update(text_style)
        if polygon_style:
            self.polygon_style.update(polygon_style)

    @staticmethod
    def read_csv(p):
        return pandas.read_csv(p, sep=None, engine='python')

    @staticmethod
    def prepare_amk_input(dframe):
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

    @staticmethod
    def prepare_polygon_coordinates(awd_out):
        """
        :param awd_out: 3d array returned by ArrowMaker.__call__(..)
        :return: 
        """
        for arrow in awd_out:
            yield ' '.join('{},{}'.format(x, y) for (x, y) in arrow)

    @classmethod
    def prepare_plot_data(cls, dframe, **amk_params):
        designer = ArrowDesigner(**amk_params)
        amk_in = cls.prepare_amk_input(dframe)
        amk_out = designer(amk_in)
        arrows = cls.prepare_polygon_coordinates(amk_out)
        return zip(arrows, dframe['color'], dframe['label'])

    def render_polygon(self, points, color='black', **polygon_attrib):
        # E.polygon(*children, **attrib)
        style = dict(self.polygon_style)
        style['fill'] = color
        elem = E.polygon(points=points, style=style, **polygon_attrib)
        return tostring(elem, encoding='unicode')

    def render_text(self, content, x, y, rx, ry, angle=0, style=None):
        # style = dict(self.text_style)
        attributes = {
            'x': '{}'.format(x),
            'y': '{}'.format(y),
            'transform': 'rotate({} {},{})'.format(angle, rx, ry),
            'style': self.text_style,
        }
        elem = E.text(content, **attributes)
        return tostring(elem, encoding='unicode')



