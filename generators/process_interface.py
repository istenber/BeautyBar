#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname('..')))


class ProcessInterface(object):
    """All chart processing should go through this interface."""

    def __init__(self):
        if self.__class__ is ProcessInterface:
            raise NotImplementedError

    def set_range(self, min, max):
        pass

    def set_attribute(self, attribute, value):
        setattr(self, attribute, value)

    def add_row(self, name, value, index=None):
        pass

    def output(self):
        return ""


def tester(usage_msg):
    import random
    import getopt
    import generators

    def usage(msg=None):
        if msg is not None: sys.stderr.write("ERROR MSG: " + str(msg))
        sys.stderr.write(usage_msg)
        sys.exit(-1)

    def rand_vals(len=4):
        n = ""
        for c in range(0, len):
            n += chr(int(random.random() * (ord('z') - ord('a'))) + ord('a'))
        return (n, int(random.random() * 50))

    def set_data(diagram, dataset):
        datasets = { 'print' : [('Yahoo', 30), ('Google', 40), ('Ask.com', 12),
                                 ('AOL', 21), ('Altavista', 3), ('MSN', 7)],
                     'test' : [ ('Short', 30), ('Very long title name', 50),
                                ('S', 0), ('ao', 1), ('Test', 25), ('x', 10)],
                     'test2' : [ ('One', 20), ('Twooooooo', 1), ('Thre', 50)],
                     'random' : [ rand_vals(6) for i in range(0, 6) ],
                     'random2' : [ rand_vals(6) for i in range(0, 8) ] }
        diagram.set_range(0, 50)
        for val in datasets[dataset]:
            diagram.add_row(val[0], val[1])

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", [])
    except getopt.error:
        usage("extra args...")
    if len(args) == 2:
        dataset = args[0]
        if dataset not in ['print', 'test', 'test2', 'random', 'random2']:
            usage("incorrect dataset: " + dataset)
        filename = args[1]
    elif len(args) == 1:
        dataset = 'print'
        filename = args[0]
    else:
        usage()
    if filename[:10] == "generators":
        filename = filename[11:]
    diagram = generators.get_instance(filename[:-3])
    if diagram is None:
        usage("import failed from \"" + filename + "\"")
    set_data(diagram, dataset)
    return diagram


def main():
    import resource
    def cpu_time():
        return resource.getrusage(resource.RUSAGE_SELF)[0]

    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    diagram = tester(
"""
Usage: ./generators/process_interface.py <dataset> <filename.py>

      where optional <dataset> is one of following,
  print    \t (default) Nice looking dataset for montage and presentations
  test     \t Test data with edge values
  test2    \t New interface test data set with more values
  random   \t Random values for testing
  random2  \t Random values with new interface
""")
    start = cpu_time();
    out = diagram.output()
    out = out.replace("/dbimages", "dynamic_images")
    out = out.replace("/images", "static/images")
    end = cpu_time();
    logging.info("CPU time used: " + str(end - start))
    print out


if __name__ == "__main__":
    main()
