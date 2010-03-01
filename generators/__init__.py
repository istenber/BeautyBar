#!/usr/bin/env python2.5
"""
Simple functions to get list of generators, generator instance by name,
and generator rating

  >>> get_instance('plain').get_ui_name()
  'Plain'
  >>> get_list()[0].get_ui_name()
  'Gradient Bars'
  >>> get_rating('plain')
  4

"""

import logging


__all__ = ['get_instance', 'get_rating', 'get_list']

generators = {
    'nature'     : 4,
    'standard'   : 3,
    'plain'      : 4,
    'equalizer'  : 2,
    'rocks'      : 2,
    'blocks'     : 1,
    'shiny'      : 1,
    'balls'      : 1,
    'paper'      : 1,
    'slices'     : 1,
    'plates'     : 2,
    'bottombar'  : 3,
    'gradient'   : 5,
    'cityview'   : 3,
    'champions'  : 3,
    'towers'     : 3,
    }


def get_instance(name):
    classname = name.capitalize()
    modulename = "generators." + name
    try:
        exec("from " + modulename + " import " + classname)
        return eval(classname)()
    except ImportError, error:
        logging.error("missing generator: " + modulename)
    return None

def get_rating(name):
    return generators[name]

def get_list(rated=True):
    if rated:
        names = map(lambda(k, v): k,
                    sorted(generators.items(),
                           key=lambda(k, v): v,
                           reverse=True))
    else:
        names = generators.keys()
    return [get_instance(name) for name in names]


if __name__ == '__main__':
    import sys
    sys.path.append('/home/sankari/dev/beautybar')
    logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()
