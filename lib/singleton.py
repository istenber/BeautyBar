#!/usr/bin/env python

class Singleton(object):
    __instance = None 

    def __new__(cls):
        if cls != type(cls.__instance):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @classmethod
    def instance(cls):
        return cls.__instance

# ------------------- test program --------------------

class TestSingleton(Singleton):
    def __init__(self):
        self.name = "TestSingleton"

class T2S(Singleton):
    def __init__(self):
        self.name = "T2S"

def main():
    t1 = TestSingleton()
    t2 = TestSingleton()
    t2s = T2S()
    print "t1: " + str(t1)
    print "t2: " + str(t2)
    if str(t1) == str(t2): print "ok."
    else: print "failed."
    print "t2: " + str(t2s)
    if str(t1) == str(t2s): print "failed."
    else: print "ok."
    if t1.name == "TestSingleton": print "ok."
    else: print "failed."
    if t2s.name == "T2S": print "ok."
    else: print "failed."

if __name__ == "__main__":
    main()
