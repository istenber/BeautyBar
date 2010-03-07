import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache
import ui.dao

class ChartPage(webapp.RequestHandler):

    # TODO: output should be png image!
    # TODO: unknown options should cause error
    # TODO: unsupported options should cause error

    def _error_chart(self, msg):
        logging.info(msg)
        return ui.dao.Generator.error(msg)

    def _get_chart(self):
        self.size = self.request.get("chs")
        if self.size == "":
            self.size = "300x200"
            return self._error_chart("Missing chs")
        filename = self.request.get("cht")
        if filename == "":
            return self._error_chart("Missing cht")
        # TODO: now style loading is based on session, fix it to
        #       use style when there is style naming
        session = ui.dao.Session.load_file(filename)
        if session is None:
            return self._error_chart("cht \"%s\" not found" % filename)
        data = self._get_data()
        if data == "":
            return self._error_chart(self.data_error)
        return session.style.get_active_generator().build_chart(data)

    # TODO: move encoders to model.data
    def _convert_values(self, value_str, encoding):
        if encoding == "t:":
            return self._text_encoding(value_str)
        if encoding == "e:":
            return self._extended_encoding(value_str)
        if encoding == "s:":
            return self._simple_encoding(value_str)
        self.data_error = "Incorrect data encoding: \"%s\"" % encoding[0]
        return ""

    def _text_encoding(self, value_str):
        chds = self.request.get("chds")
        if chds == "":
            self.data_min = 0
            self.data_max = 100
        else:
            [self.data_min, self.data_max] = chds.split(",")
        return value_str.split(",")

    def _extended_encoding(self, value_str):
        self.data_min = 0
        self.data_max = 4095
        values = []
        for index in range(0, len(value_str), 2):
            a = ord(value_str[index])
            b = ord(value_str[index+1])
            if (a == ord("_") and b == ord("_")):
                # TODO: is missing value 0?
                values.append(0)
                continue
            if (a >= ord("A") and a <= ord("Z")):
                val = (a - ord("A")) * 64
            elif (a >= ord("a") and a <= ord("z")):
                val = (a - ord("a") + 26) * 64
            elif (a >= ord("0") and a <= ord("9")):
                val = (a - ord("0") + 52) * 64
            elif a == ord("-"):
                val = 62 * 64
            elif a == ord("."):
                val = 63 * 64
            else:
                self.data_error = ("Cannot encode char: \"" +
                                   value_str[index] + "\"")
                return ""
            if (b >= ord("A") and b <= ord("Z")):
                val += (b - ord("A"))
            elif (b >= ord("a") and b <= ord("z")):
                val += (b - ord("a") + 26)
            elif (b >= ord("0") and b <= ord("9")):
                val += (b - ord("0") + 52)
            elif b == ord("-"):
                val += 62
            elif b == ord("."):
                val += 63
            else:
                self.data_error = ("Cannot encode char: \"" +
                                   value_str[index+1] + "\"")
                return ""
            values.append(val)
        return values

    def _simple_encoding(self, value_str):
        self.data_min = 0
        self.data_max = 61
        values = []
        for index in range(0, len(value_str)):
            char = ord(value_str[index])
            if (char >= ord("A") and char <= ord("Z")):
                values.append(char - ord("A"))
            elif (char >= ord("a") and char <= ord("z")):
                values.append(char - ord("a") + 26)
            elif (char >= ord("0") and char <= ord("9")):
                values.append(char - ord("0") + 52)
            elif char == ord("_"):
                # TODO: is missing value 0?
                values.append(0)
            else:
                self.data_error = ("Cannot encode char: \"" +
                                   value_str[index] + "\"")
                return ""
        return values

    def _get_data(self):
        value_str = self.request.get("chd")
        if value_str == "":
            self.data_error = "Missing chd"
            return ""
        name_str = self.request.get("chl")
        if name_str == "":
            self.data_error = "Missing chl"
            return ""
        names = name_str.split("|")
        encoding = value_str[:2]
        values = self._convert_values(value_str[2:], encoding)
        if values == "":
            return ""
        if len(values) != len(names):
            self.data_error = "chl and chd should have same lenght"
            return ""
        if not ui.dao.Data.is_valid_len(len(values)):
            self.data_error = "Invalid number of rows"
            return ""
        d = ui.dao.Data.from_arrays(self.data_min, self.data_max, names, values)
        if d is None:
            self.data_error = "Problems with data"
            return ""
        return d

    def cache_key(self):
        key = ""
        for arg in self.request.arguments():
            key += arg + "=" + self.request.get(arg) + "&"
        key = key[:-1]
        logging.debug("Memcache key: " + key)
        return key

    def in_cache(self, key):
        self.cached_data = memcache.get(key)
        return self.cached_data is not None

    def get(self):
        self.response.headers['Content-Type'] = "image/svg+xml"
        key = self.cache_key()
        if self.in_cache(key):
            logging.debug("Found in cache")
            out = self.cached_data
        else:
            # TODO: lets save this with output, or is it required?
            # o = Output()
            chart = self._get_chart()
            chart.resize_str(self.size)
            out = chart.output()
            memcache.add(key, out, 60)
        self.response.out.write(out)
