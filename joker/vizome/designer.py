#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import numpy as np
from numpy import tan

"""
Anatomy of an Arrow
by Hailong on 2015 Xmas

                           /+ 1                     +
                         / /                        |
                       /  /                         |
                     /   /                          |
                   /    /                           |
                 /     /                            | < height2
               /      /                             |
             /       / <beta                    3   |
           /      2 +---------------------------+   |      +
         / <alpha  /                            |   |      |  < height1
     0  <---------+-----------------------------+   +      +
         \         \                            |              alpha < beta
           \      . 5---------------------------+            height1 < height2
                  . .                           4
                  . .
                  . .
        + - - - - +     threshold1
        + - - - - - +   threshold2

        + < - - - - - - length  - - - - - - - > +



length is the main variable.
alpha, height2 are always constant

Threshold 2
As length decreases, point2 and point3 will join, and height1 begin to decrease.

Threshold 1
As length decreases continuously, height1 will become 0, and beta begin to decrease.
"""


def cot(x):
    return 1. / tan(x)


def make_array(data):
    """
    >>> make_array(3) 
    array([3])
    >>>  make_array(i for i in range(3))
    array([0, 1, 2])
    >>> make_array([1, 2, 3])
    array([1, 2, 3]) 
    >>> make_array(np.arange(3))   # simply pass through
    array([0, 1, 2])
    """
    if isinstance(data, np.ndarray):
        arr = data
    elif isinstance(data, (list, int, float)):
        arr = np.array(data)
    else:
        arr = np.array(list(data))
    if arr.ndim == 0:
        arr.shape = -1
    return arr


class ArrowDesigner(object):
    def __init__(self, alpha=.7, beta=1., height1=16, height2=32):
        self.alpha = alpha
        self.beta = beta
        self.height1 = height1
        self.height2 = height2
        self.threshold1 = height2 * (cot(alpha) - cot(beta))
        self.threshold2 = self.threshold1 + height1 * cot(beta)

    def prototype(self, length=3.):
        """
        For understanding of the formula
        Not intended for actual use
        :param length:
        :return:
        """
        data = np.empty([8, 2])
        if length >= self.threshold2:
            data[1] = self.height2 * cot(self.alpha), self.height2
            data[2] = self.threshold2, self.height1
            data[3] = length, self.height1

        # elif self.threshold1 < length < self.threshold2:
        elif self.threshold1 < length < self.threshold2:
            data[1] = self.height2 * cot(self.alpha), self.height2
            data[2] = length, (length - self.threshold1) * tan(self.beta)
            data[3] = length, (length - self.threshold1) * tan(self.beta)
        else:
            data[1] = self.height2 * cot(self.alpha), self.height2
            data[2] = length, 0
            data[3] = length, 0

        data[4:7] = data[1:4][::-1] * np.array([1, -1])
        data[0] = 0, 0
        data[7] = 0, 0
        return data

    def calculate(self, lengths):
        """
        Algorithm
        :param lengths: 1d array, all values should be positive
        :return:
        """
        data = np.zeros([len(lengths), 8, 2])

        # point 0 is (0, 0)
        # dt[:, 0, 0] = 0
        # dt[:, 0, 1] = 0

        # point 1 is fixed
        data[:, 1, 0] = self.height2 * cot(self.alpha)
        data[:, 1, 1] = self.height2

        # masks
        mask0 = lengths <= self.threshold1
        mask1 = (self.threshold1 < lengths) & (lengths < self.threshold2)
        mask2 = lengths >= self.threshold2

        data[:, 2, 0][mask0] = lengths[mask0]
        data[:, 2, 0][mask1] = lengths[mask1]
        data[:, 2, 0][mask2] = self.threshold2

        data[:, 3, 0] = lengths

        # point 2 and point 3 are of same height
        # dt[:, 2, 1][mask0] = 0
        # dt[:, 3, 1][mask0] = 0
        data[:, 2, 1][mask1] = ((lengths - self.threshold1) * tan(self.beta))[mask1]
        data[:, 3, 1][mask1] = ((lengths - self.threshold1) * tan(self.beta))[mask1]
        data[:, 2, 1][mask2] = self.height1
        data[:, 3, 1][mask2] = self.height1

        data[:, 4:7, :] = data[:, 1:4, :][:, ::-1, :] * np.array([1, -1])
        return data

    def __call__(self, awd_in):
        """
        :param awd_in: 1d or 2d array
       
        #1
        .calc([a0_length, a1_length, a2_length, ..]), which is equivolent to
        .calc([
            (a0_lenth, 0),
            (a1_lenth, 0),
            (a2_lenth, 0),
        ])
        
        
        #2
        .calc([
            (a0x_start, a0x_end),
            (a1x_start, a1x_end),
            (a3x_start, a3x_end), ...
        ])
        
        #3 
        .calc([
            (a0x_start, a0x_end, a0y),
            (a1x_start, a1x_end, a1y),
            (a2x_start, a2x_end, a2y), ...
        ])
        
        :return: a 3d array
        [
            [
                [x0, y0], [x1, y1], [x2, y2], [x3, y3],     #  arrow 1
                [x4, y4], [x5, y5], [x6, y6], [x7, y7],
            ],
            
            [
                [x0, y0], [x1, y1], [x2, y2], [x3, y3],     #  arrow 2
                [x4, y4], [x5, y5], [x6, y6], [x7, y7],
            ],
            ...
        ] 
        
        """
        awd_in = make_array(awd_in)

        if awd_in.ndim > 2:
            raise ValueError("number of dimensions of 'arr' should be 1 or 2")

        # simply an array of lengths
        if awd_in.ndim == 1 or awd_in.shape[-1] == 1:
            lengths = awd_in.reshape([-1])
            orients = np.sign(lengths)
            awd_out = self.calculate(np.abs(lengths))
            awd_out[:, :, 0] *= orients.reshape([-1, 1])
            return awd_out

        # treat last dim as (start, end)
        if awd_in.shape[-1] == 2:
            lengths = awd_in[:, 0] - awd_in[:, 1]
            orients = np.sign(lengths)  # length can NOT be 0
            awd_out = self.calculate(abs(lengths))
            awd_out[:, :, 0] *= orients.reshape([-1, 1])
            awd_out[:, :, 0] += awd_in[:, 1].reshape([-1, 1])
            return awd_out

        # treat last dim as (x_start, x_end, y)
        if awd_in.shape[-1] == 3:
            awd_out = self(awd_in[:, :2])
            awd_out[:, :, 1] += awd_in[:, 2].reshape([-1, 1])
            return awd_out
