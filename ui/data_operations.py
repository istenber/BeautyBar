import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.utils import unquote
from ui.basepage import SessionPage
import ui.dao


class SaveData(SessionPage):

    def get(self):
        self.get_session()
        filename = self.request.get("name")
        old_file = ui.dao.Session.load_file(filename)
        if old_file is None:
            self.response.out.write("Saved as " + filename)
        else:
            self.session.name = "_deleted"
            self.session.put()
            self.response.out.write("Replaced old " + filename)
        newone = self.session.copy_model_instance()
        newone.name = filename
        newone.cookie = ""
        newone.put()


class LoadData(SessionPage):

    def get(self):
        self.get_session()
        filename = self.request.get("name")
        old_file = ui.dao.Session.load_file(filename)
        if old_file is None:
            self.response.out.write("Cannot find " + filename)
            return
        newone = old_file.copy_model_instance()
        newone.name = ""
        newone.cookie = self.session.cookie
        newone.put()
        self.session.name = "_deleted"
        self.session.cookie = ""
        self.session.put()
        self.response.out.write(filename + " loaded")


class ImportData(SessionPage):

    def post(self):
        self.get_session()
        filename = self.request.get("f_file")
        d = self._parse_csv(file)
        if d is not None:
            d.put()
            self.session.data = d
            self.session.put()
        self.redirect("/")

    # TODO: move parsing to model.data
    # Not fully compliant with csv, as ...
    # 1. "e accept following separators ,.:\t
    # 2. Don't allow multiline messages
    # 3. Allow only lines with two values, all others are ignored
    def _parse_csv(self, csv):
        lines = []
        for line in csv.splitlines():
            if line.strip() == "": continue
            lines.append(line)
        if len(lines) < Data.max_len():
            logging.info("# Too few lines (" + str(len(lines)) + ") in CSV")
            return None
        for delim in [",", ".", ":", "\t"]:
            d = self.objfac('Data', name="", min=0.0, max=50.0, locked=False)
            line_nro = 1
            for line in lines:
                try:
                    vals = line.split(delim)
                except ValueError, e:
                    logging.info("# Error in CSV line: \"" + line + "\"")
                    return None
                if len(vals) == 2:
                    name = unquote(vals[0])
                    value = unquote(vals[1])
                    item = self.objfac('Item',
                                       name=name, value=value, row=line_nro)
                    if not d.add_item(item):
                        logging.info("# Incorrect item")
                        return None
                    else:
                        line_nro += 1
            if d.is_valid(): return d
        logging.info("# Cannot parse CSV")
        return None


class CleanData(webapp.RequestHandler):
    def get(self):
        self._clean()
    def post(self):
        self._clean()
    def _clean(self):
        session = ui.dao.Session.default(self.request.remote_addr)
        session.put()
        self.response.headers['Set-Cookie'] = "session=" + session.cookie
        self.redirect("/")
