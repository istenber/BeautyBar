import logging

from ui.basepage import ExtraPage


class LearnPage(ExtraPage):
    
    def _is_valid_page(self, page):
        return page in ['basics', 'style']

    def get_values(self):
        page = self.request.get("page")
        if page != "" and self._is_valid_page(page):
            return { 'template' : "learn" + page }
        return { }


class AboutPage(ExtraPage):
    
    def get_values(self):
        return { }
