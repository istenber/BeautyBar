import logging
import os

from ui.basepage import SessionPage
from google.appengine.ext.webapp import template
import ui.dao

class AjaxMain(SessionPage):

    def _is_valid_part(self, part):
        return part in ['info', 'edit']

    def get(self):
        part = self.request.get("part")
        if not self._is_valid_part(part):
            self.response.headers['Content-Type'] = "text/plain"
            logging.info("# Trying get invalid part \"" + str(part) + "\"")
            self.response.out.write("error")
            return
        self.get_session()
        values = eval("self.get_" + part)()
        self.response.headers['Content-Type'] = "text/html"
        file = "../templates/main/" + values['template'] + ".html"
        path = os.path.join(os.path.dirname(__file__), file)
        self.response.out.write(template.render(path, values))

    # TODO: implement part caching in javascript

    def _chart_api_link(self):
        style = self.session.name
        values = ""
        names = ""
        for item in self.session.data.as_list():
            values += str(item.value) + ","
            names += item.name + "|"
        return ("http://beauty-bar.appspot.com/" +
                "chart?cht=" + style + "&chd=t:" + values[:-1] +
                "&chs=300x200&chl=" + names[:-1])

    def get_info(self):
        g = self.session.style.get_active_generator()
        chart = g.me()
        return { 'template'    : 'info',
                 'name'        : chart.get_ui_name(),
                 'description' : chart.get_description(),
                 # TODO: this is not in use
                 # 'chart_api'   : self._chart_api_link(),
                 'rating'      : range(0, chart.get_rating()),
                 }

    def get_edit(self):
        s = self.request.get("s")
        if s == "data":
            return { 'template' : 'editdata',
                     'items'    : self.session.data.as_list(),
                     'r_min'    : self.session.data.min,
                     'r_max'    : self.session.data.max,
                     }
        if s == "style":
            return { 'template'   : 'editstyle',
                     'cur_gen'    : self.session.style.get_active_generator(),
                     }
        if s == "file":
            return { 'template' : 'editfile' }
        logging.info("# part edit missing or incorrect sub \"" + s + "\"")
        return { 'template' : 'editdata' }
