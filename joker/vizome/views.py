#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import flask

viz_blueprint = flask.Blueprint('viz', __name__)


@viz_blueprint.route('/')
def default():
    response = flask.make_response('start!')
    # response.headers['Content-Type'] = 'image/png'
    # response.headers['Content-Disposition'] = 'inline'
    # response.headers['Content-Disposition'] = 'attachment; filename=img.png'
    return response


@viz_blueprint.route('/test')
def test():
    response = flask.make_response('start!')
    # response.headers['Content-Type'] = 'image/png'
    # response.headers['Content-Disposition'] = 'inline'
    # response.headers['Content-Disposition'] = 'attachment; filename=img.png'
    return response

