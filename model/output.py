#!/usr/bin/env python

import logging

class Output(object):

    def __init__(self, name=""):
        self.name = name
        self.content_type = "text/plain"
        self.content = None
        self.data = None
        self.style = None

    def copy(self, data=None, style=None):
        o = Output()
        o.name = self.name
        o.content_type = self.content_type
        o.data = data
        o.style = style
        return o


def main():
    pass

if __name__ == "__main__":
    main()
