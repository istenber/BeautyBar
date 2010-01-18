import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.data import Item, Data
from model.session import Session
from model.output import Output
from model.style import Style
from ui.dao import DAO
from model.utils import unquote


def _generate_session_id():
    import uuid
    return str(uuid.uuid4())

def make_clean_session(ip_address):
    ses = Session(name=_generate_session_id())
    data = Data.default()
    data.locked = True
    style = Style.default()
    style.locked = True
    output = Output()
    output.data = data
    output.style = style
    ses.data = data
    ses.output = output
    ses.style = style
    ses.ip_address = str(ip_address)
    DAO.save(ses)
    return ses


# TODO: note saves data AND style
class SaveData(webapp.RequestHandler):

    def _old_data(self, name):
        return DAO.load(name=name, class_name="Session")

    def get(self):
        new_name = self.request.get("name")
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
            session = DAO.load(name=name, class_name="Session")
        old_data = self._old_data(new_name)
        if old_data is None:
            self.response.out.write("Saved as " + new_name)
        else:
            old_data.name = "_deleted"
            DAO.save(old_data)
            self.response.out.write("Replaced old " + new_name)
        copy = session.copy()
        copy.name = new_name
        DAO.save(copy)


# TODO: note loads data AND style
class LoadData(webapp.RequestHandler):

    def get(self):
        old_name = self.request.get("name")
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
        old = DAO.load(name=old_name, class_name="Session")
        if old is None:
            self.response.out.write("Cannot find " + old_name)
            return

        session = old.copy()
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
        session = make_clean_session(self.request.remote_addr)
        self.response.headers['Set-Cookie'] = "session=" + session.name
        self.redirect("/")
