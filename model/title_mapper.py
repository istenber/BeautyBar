#!/usr/bin/env python
"""
Title mapper will tell what titles are...

  >>> titles = ['some', 'random', 'words', 'with', 'no', 'meaning']
  >>> t = TitleMapper(titles)
  >>> print t.get_meaning()
  None
  

"""

import logging


list_of_title_sets = ['Years', 'Countries']


class TitleMapper(object):
    """ TitleMapper class
    """

    def __init__(self, titles):
        self.titles = titles

    def get_meaning(self):
        if not hasattr(self, "meaning"):
            self.meaning = None
            for title_set in list_of_title_sets:
                meaning = eval(title_set).solver(self.titles)
                if meaning is not None:
                    self.meaning = meaning
                    return self.meaning
        return self.meaning        

    def __unicode__(self):
        return self.meaning


class TitleSet(object):

    def __init__(self, titles):
        self.titles = titles

    @classmethod
    def solver(cls, titles):
        raise Exception("override me")


class Years(TitleSet):

    @classmethod
    def solver(cls, titles):
        """ Years support two kind of formats

        Full year with four digits...

          >>> years = ['2001', '2002', '2003', '2004', '2005', '2006']
          >>> type(TitleMapper(years).get_meaning())
          <class '__main__.Years'>

        Slash and two digits...

          >>> years = ['-01', '-02', '-03', '-04', '-05', '-06']
          >>> type(TitleMapper(years).get_meaning())
          <class '__main__.Years'>

        Numbers should be in raising order
          
          >>> years = ['-06', '-05', '-04', '-03', '-02', '-01']
          >>> type(TitleMapper(years).get_meaning())
          <type 'NoneType'>

        """
        y = Years(titles)
        if y.are_four_digit_years():
            return y
        if y.are_slash_two_digit_years():
            return y
        return None

    def are_four_digit_years(self):
        prev = 0
        for title in self.titles:
            if len(title) != 4:
                return False
            try:
                current = int(title)                
            except ValueError:
                return False
            if current < prev:
                return False
            prev = current
        self.four_digit_years = True
        return True

    def are_slash_two_digit_years(self):
        prev = 0
        for title in self.titles:
            if len(title) != 3:
                return False
            try:
                current = int(title[1:])
            except ValueError:
                return False
            if current < prev:
                return False
            prev = current
        self.slash_two_digit_years = True
        return True


class Countries(TitleSet):
    # TODO: add more
    __list_of_countries = ['poland', 'germany', 'sweden', 'finland',
                           'russia', 'france', 'u.s.a.', 'usa', 'china',
                           'brazil', 'norway' ]

    @classmethod
    def solver(cls, titles):
        """ Countries support only some countries. Makes difference
        between lower and upper case, and accepts if five out of six
        are known coutries.

        Uzzbecistan is not are real country, but still accept as
        other five are.

          >>> countries = ['sweden', 'Finland', 'UZZbecistan', 
          ...              'Russia', 'Germany', 'FRANCE']
          >>> type(TitleMapper(countries).get_meaning())
          <class '__main__.Countries'>

        One few countries, so no...

          >>> countries = ['U.S.A.', 'Afrika', 'Tennis', 
          ...              '2001', 'Poland', 'earth']
          >>> type(TitleMapper(countries).get_meaning())
          <type 'NoneType'>

        """
        c = Countries(titles)
        if c.count_countries() >= 5:
            return c
        return None

    def is_country(self, title):
        return title.lower() in Countries.__list_of_countries

    def count_countries(self):
        self.country_count = 0
        for title in self.titles:
            if self.is_country(title):
               self.country_count += 1
        return self.country_count

# TODO: cities
# TODO: departments
# TODO: languages
# TODO: names (mark, john, ...)

if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()

