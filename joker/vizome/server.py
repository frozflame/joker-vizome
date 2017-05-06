#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import argparse
import os
import flask
import jinja2
import joker.vizome

# from molbiox.frame.environ import get_template, from_default
from joker.cast.serialize import JSONEncoderExtended

jinja2_env = None


def get_template(filename):
    global jinja2_env
    if jinja2_env is None:
        tpldir = os.path.join(os.path.dirname(joker.vizome.__file__), 'templates')
        jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(tpldir)
        )
    return jinja2_env.get_template(filename)


def get_wsgi_application(debug=False, offline=True):
    from joker.vizome.views import viz_blueprint
    app_dir = os.path.dirname(joker.vizome.__file__)

    flask_params = {
        'static_folder': os.path.join(app_dir, 'static'),
        'template_folder': os.path.join(app_dir, 'templates'),
    }

    app = flask.Flask('yamdrok', **flask_params)
    app.debug = debug
    app.json_encoder = JSONEncoderExtended

    if offline:
        app.test_request_context().push()

    @app.before_request
    def _set_global():
        g = flask.g
        g.static_url = '/static'

    blueprints = [viz_blueprint]
    for bp in blueprints:
        app.register_blueprint(bp)
        # print(bp)
    return app


def run_dev_server(debug=True, host='0.0.0.0', port=8005, **_):
    app = get_wsgi_application(debug)
    try:
        app.run(host=host, port=port, debug=debug, use_reloader=True)
    except:
        raise


def parse_args():
    parser = argparse.ArgumentParser(description='vizome')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-p', '--port', type=int, default=8005)
    parser.add_argument('--host', default='0.0.0.0')
    return parser.parse_args()


def entry_point():
    args = parse_args()
    run_dev_server(**vars(args))
