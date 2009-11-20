#!/usr/bin/env python

import logging

class Session(object):

    def __init__(self, name=""):
        self.name = name
        self.data = None
        self.style = None
        self.output = None

    def copy(self):
        s = Session()
        s.name = self.name
        s.data = self.data.copy()
        s.style = self.style.copy()
        s.output = self.output.copy(s.data, s.style)
        return s

def main():
    pass

if __name__ == "__main__":
    main()
