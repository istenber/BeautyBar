#!/usr/bin/env python

import resource
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname('..')))

from model.generator_factory import GeneratorFactory


def TIME_cpu_time():
    return resource.getrusage(resource.RUSAGE_SELF)[0]

def RESOURCE_cpu_time():
    return time.clock()

cpu_time = RESOURCE_cpu_time

def measure(diagram):
    start = cpu_time()
    diagram.output()
    end = cpu_time()
    return (end - start) * 1000

def main():
    print "CPU Times..."
    print "------------------------------"
    for diagram in GeneratorFactory().list():
        diagram.set_range(0, 50)
        diagram.add_row('a', 10)
        diagram.add_row('b', 15)
        diagram.add_row('c', 20)
        diagram.add_row('d', 30)
        diagram.add_row('e', 40)
        diagram.add_row('f', 50)
        print "| %15s | %5.0f ms |" % (str(diagram.get_ui_name()),
                                       measure(diagram))
    print "------------------------------"
    

if __name__ == "__main__":
    main()
