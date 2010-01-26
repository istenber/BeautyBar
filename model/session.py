#!/usr/bin/env python

import logging


class Session(object):

    def __init__(self, name="no name"):
        self.name = name
        self.cookie = cookie
        self.ip_address = ""
        self.data = None
        self.style = None
        self.output = None

    # boilerplate ---------------------------
    @classmethod
    def objfac(cls, new_cls, **kwds):
        # TODO: imports?
        #   from data import Data
        # etc.
        return eval(new_cls)(**kwds)
    # ---------------------------------------

    @classmethod
    def _generate_session_id(cls):
        import uuid
        return str(uuid.uuid4())

    @classmethod
    def default(cls, ip_address="0.0.0.0"):
        data = cls.objfac('Data').default()
        data.locked = True
        style = cls.objfac('Style').default()
        style.locked = True
        output = cls.objfac('Output')
        output.data = data
        output.style = style
        # TODO: combine...
        session = cls.objfac('Session')
        session.name = "no name"
        session.cookie = cls._generate_session_id()
        session.data = data
        session.output = output
        session.style = style
        session.ip_address = str(ip_address)
        return session


def main():
    pass

if __name__ == "__main__":
    main()
