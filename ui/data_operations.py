import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.utils import unquote
import ui.dao

# TODO: SaveData, LoadData and ImportData don't work!!!

# TODO: note saves data AND style
class SaveData(webapp.RequestHandler):

    def get(self):
        return

    def _old_session(self, name):
        return DAO.load(name=name, class_name="Session")

    def not_working(self):
        new_name = self.request.get("name")
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
            session = DAO.load(name=name, class_name="Session")
        old_session = self._old_session(new_name)
        if old_session is None:
            self.response.out.write("Saved as " + new_name)
        else:
            old_session.name = "_deleted"
            DAO.save(old_session)
            self.response.out.write("Replaced old " + new_name)
        newone = copy.deepcopy(session)
        # del newone.__dict__["__dbkey__"]
        newone.name = new_name
        DAO.save(newone)


# TODO: note loads data AND style
class LoadData(webapp.RequestHandler):

    def get(self):
        return

    def not_working(self):
        old_name = self.request.get("name")
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
        old = DAO.load(name=old_name, class_name="Session")
        if old is None:
            self.response.out.write("Cannot find " + old_name)
            return

        session = copy.deepcopy(old)
        session.name = name

        # TODO: remove old files!!!
        # TODO: make db to support removes
        #       then remove this hack!
        cur = DAO.load(name=name, class_name="Session")
        cur.name = "_deleted"
        DAO.save(cur)

        DAO.save(session)
        self.response.out.write(old_name + " loaded")


class ImportData(webapp.RequestHandler):

    def post(self):
        return

    def not_working(self):
        logging.info("import data")
        file = self.request.get("f_file")
        # TODO: if there is no session!!?
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
            session = DAO.load(name=name, class_name="Session")
        d = self._parse_csv(file)
        if d is not None:
            session.data = d
            DAO.save(session)
        self.redirect("/")

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
            d = Data()
            for line in lines:
                try:
                    vals = line.split(delim)
                except ValueError, e:
                    logging.info("# Error in CSV line: \"" + line + "\"")
                    return None
                if len(vals) == 2:
                    name = unquote(vals[0])
                    value = unquote(vals[1])
                    if not d.add_item(Item(name, value)):
                        logging.info("# Incorrect item")
                        return None
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
        self.response.headers['Set-Cookie'] = "session=" + session.cookie
        self.redirect("/")
