from flask import Flask
from functools import partial, update_wrapper


def compose(g, f):
    return lambda *args, **kwargs: g(f(*args, **kwargs))


class FlaskWrapper(Flask):

    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)

    def route(self, rule, **options):
        apply_self = lambda f: update_wrapper(partial(f, self=None), f)
        decorator = Flask.route(self, rule, **options)
        return compose(decorator, apply_self)
