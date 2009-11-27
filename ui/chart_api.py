import logging

from google.appengine.ext import webapp
from model.data import Item, Data
from ui.dao import DAO
from model.session import Session
from model.output import Output
from model.style import Style
from model.generator_factory import GeneratorFactory

class ChartPage(webapp.RequestHandler):

    # TODO: output should be png image!

    # specification:
    # /chart?cht=p3&chd=t:60,40&chs=250x100&chl=Hello|World

    # test:
    # http://localhost:8080/chart?cht=def&chd=t:10,11,12,13,14,20&chs=250x100&chl=Hello|World|a|b|helo|worl

    def _default_style(self, msg):
        logging.info("# " + msg)
        return Style.default()

    def _get_style(self):
        name = self.request.get("cht")
        if name == "": return self._default_style("missing style")
        # TODO: now style loading is based on session, fix it to
        #       use style when there is style naming
        session = DAO.load(name=name, class_name="Session")
        if session is None:
            return self._default_style("session \"" + name + "\" not found")
        s = session.style
        if s is None:
            return self._default_style("style not found")
        # logging.info("# STYLE: \"" + s.name + "\"  \"" + session.name + "\"")
        return s

    def _default_data(self, msg):
        logging.info("# " + msg)
        return Data.default()

    def _get_data(self):
        values = self.request.get("chd")
        if values == "": return self._default_data("missing data values")
        names = self.request.get("chl")
        if names == "": return self._default_data("missing data names")
        if values[:2] != "t:": return self._default_data("incorrect data (t:)")
        v_list = values[2:].split(",")
        n_list = names.split("|")
        if len(v_list) != len(n_list):
            return self._default_data("names len is not equal to values len")
        # TODO: fixme
        if len(v_list) != 6:
            return self._default_data("wrong amount of data")
        d = Data()
        for i in range(0, 6):
            d.add_item(Item(n_list[i], v_list[i]))
            # logging.info("# (" + str(n_list[i]) + ":" + str(v_list[i]) + ")")
        return d

    def get(self):
        self.response.headers['Content-Type'] = "image/svg+xml"
        # TODO: lets save this with output, or is it required?
        # o = Output()
        s = self._get_style()
        d = self._get_data()
        # TODO: handle size (chs)
        g = s.get_active_generator()
        logging.debug("# ChartAPI")
        self.response.out.write(g.build_chart(d))
