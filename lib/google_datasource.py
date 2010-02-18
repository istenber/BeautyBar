#!/usr/bin/env python

import logging
import urllib
import re

from demjson import JSON, JSONDecodeError


# TODO: check for sig
# TODO: handle errors and warnings
class GoogleDataSource(object):
    """ Parse Google data source to table

      >>> source = 'http://spreadsheets.google.com/tq?key=pCQbetd-CptGXxxQIG7VFIQ&range=B1:D11&pub=1'
      >>> ds = GoogleDataSource()
      >>> ds.set_source(source)      
      >>> ds.is_ok()
      True
      >>> ds.get_version()
      '0.6'
      >>> ds.get_titles()
      ['Country code', 'Population', 'Population Density']
      >>> ds.get_row(1)
      'IN'
    
    """

    def __init__(self):
        self.json = JSON()

    def set_source(self, source):
        self.source = source
        f = urllib.urlopen(source)
        s = f.readline()
        self.parse(s)

    def parse(self, string):
        string = strip_query(string)
        string = remove_dates(string)
        try:
            self.object = self.json.decode(string)
        except JSONDecodeError, e:
            logging.info("Decode error: " + str(e))
            self.object = None
        # self._dump()

    def is_ok(self):
        self._check()
        if self.object is None:
            return False
        if self.object['status'] == 'ok':
            return True
        errmsg = ""
        for error in self.object['errors']:
            errmsg += "(" + error['reason'] + ":" + error['message'] + "),"
        errmsg = errmsg[:-1]
        logging.info("Status \"" + str(self.object['status']) + "\": " + errmsg)
        return False

    def get_version(self):
        self._check()
        return self.object['version']

    def get_title(self, column):
        if not hasattr(self, "titles"):
            self.get_titles()
        return self.titles[column]

    def get_titles(self):
        if not hasattr(self, "titles"):
            self._check()
            self.titles = map(lambda x: x['label'],
                              self.object['table']['cols'])
        return self.titles

    def get_row(self, row):
        if not hasattr(self, "rows"):
            self.get_rows()
        return self.rows[row]

    def get_rows(self):
        def parse_row(row):
            arr = []
            for elem in row['c']:
                if type(elem) is not dict:
                    arr.append(str(elem))
                elif elem.has_key('f'):
                    arr.append(elem['f'])
                else:
                    arr.append(str(elem['v']))
            return arr
        if not hasattr(self, "rows"):
            self._check()
            self.rows = map(parse_row,
                            self.object['table']['rows'])
        return self.rows

    def __str__(self):
        self._check()
        return self.__class__.__name__ + ": " + self.object['version']

    def _check(self):
        if not hasattr(self, "object"):
            raise GoogleDataSourceException("missing object")

    def _dump(self):
        self._check()
        logging.debug("dump/version: " + self.get_version())
        for title in self.get_titles():
            logging.debug("dump/title: " + str(title))
        for row in self.get_rows():
            logging.debug("dump/row: " + str(row))


class GoogleDataSourceException(Exception):
    pass


QUERY_PREFIX = 'google.visualization.Query.setResponse('
QUERY_POSTFIX = ');'


def strip_query(s):
    return s[len(QUERY_PREFIX):-len(QUERY_POSTFIX)]

def remove_dates(s):
    # lets replace 'v:new Date(2010,10,10)' with 'v:0' as we don't use
    # v values anyway, but new breaks json parsing
    return re.sub(r'v:new Date\(\d\d\d\d,\d\d?,\d\d?\)',r'v:0', s)


# --------------- tests -----------------

def test_valid():
    test_str = "google.visualization.Query.setResponse({version:'0.6',status:'ok',sig:'184259073',table:{cols:[{id:'B',label:'',type:'number',pattern:'#0.###############'}],rows:[{c:[{v:3213.0,f:'3213'}]},{c:[{v:3.0,f:'3'}]},{c:[{v:3213.0,f:'3213'}]},{c:[{v:32.0,f:'32'}]},{c:[{v:321.0,f:'321'}]}]}});"
    ds = GoogleDataSource()
    ds.parse(test_str)
    assert ds.is_ok()
    assert ds.get_version() == '0.6'
    assert ds.get_rows() == [ ['3213'], ['3'], ['3213'], ['32'], ['321'] ]

def test_valid_big():
    test_str = "google.visualization.Query.setResponse({version:'0.6',status:'ok',sig:'1068688546',table:{cols:[{id:'B',label:'Country code',type:'string',pattern:''},{id:'C',label:'Population',type:'number',pattern:'#0.###############'},{id:'D',label:'Population Density',type:'number',pattern:'#0.###############'}],rows:[{c:[{v:'CN'},{v:1.32297E9,f:'1322970000'},{v:137.0,f:'137'}]},{c:[{v:'IN'},{v:1.13013E9,f:'1130130000'},{v:336.0,f:'336'}]},{c:[{v:'US'},{v:3.03605941E8,f:'303605941'},{v:31.0,f:'31'}]},{c:[{v:'ID'},{v:2.31627E8,f:'231627000'},{v:117.0,f:'117'}]},{c:[{v:'BR'},{v:1.86315468E8,f:'186315468'},{v:22.0,f:'22'}]},{c:[{v:'PK'},{v:1.626525E8,f:'162652500'},{v:198.0,f:'198'}]},{c:[{v:'BD'},{v:1.58665E8,f:'158665000'},{v:1045.0,f:'1045'}]},{c:[{v:'NG'},{v:1.48093E8,f:'148093000'},{v:142.0,f:'142'}]},{c:[{v:'RU'},{v:1.41933955E8,f:'141933955'},{v:8.4,f:'8.4'}]},{c:[{v:'JP'},{v:1.2779E8,f:'127790000'},{v:339.0,f:'339'}]}]}});"
    ds = GoogleDataSource()
    ds.parse(test_str)
    assert ds.is_ok()
    assert ds.get_version() == '0.6'
    assert ds.get_titles() == ['Country code',
                               'Population',
                               'Population Density']
    assert ds.get_title(1) == 'Population'
    assert ds.get_row(1) == ['IN', '1130130000', '336']

def test_valid_with_date():
    test_str = "google.visualization.Query.setResponse({version:'0.6',status:'ok',sig:'898078434',table:{cols:[{id:'D',label:'',type:'date',pattern:'M/d/yyyy'},{id:'E',label:'',type:'number',pattern:'#0.###############'}],rows:[{c:[,{v:70.0,f:'70'}]},{c:[{v:new Date(2009,11,31),f:'12/31/2009'},{v:66.73819999999999,f:'66.7382'}]},{c:[{v:new Date(2009,8,30),f:'9/30/2009'},{v:59.4485,f:'59.4485'}]},{c:[{v:new Date(2009,5,30),f:'6/30/2009'},{v:55.229,f:'55.229'}]},{c:[{v:new Date(2009,2,31),f:'3/31/2009'},{v:55.0899,f:'55.0899'}]},{c:[{v:new Date(2008,11,31),f:'12/31/2008'},{v:57.00899999999999,f:'57.009'}]}]}});"
    ds = GoogleDataSource()
    ds.parse(test_str)
    assert ds.is_ok()
    assert ds.get_row(3) == ['6/30/2009', '55.229']

def test_invalid_json():
    ds = GoogleDataSource()
    ds.parse("google.visualization.Query.setResponse({version::});")
    assert not ds.is_ok()

def test_invalid_msg():
    ds = GoogleDataSource()
    ds.parse("...")
    assert not ds.is_ok()

def doctests():
    import doctest
    doctest.testmod()

def main():
    test_valid()
    test_valid_big()
    test_valid_with_date()
    test_invalid_json()
    test_invalid_msg()
    # doctests()

if __name__ == '__main__':
    main()
