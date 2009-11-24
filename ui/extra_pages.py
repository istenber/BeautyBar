import logging

from ui.basepage import BasePage


class LearnPage(BasePage):
    
    def _is_valid_page(self, page):
        return page in ['basics', 'style']

    def _get_values(self):
        page = self.request.get("page")
        if page != "" and self._is_valid_page(page):
            return { 'template' : "learn" + page }
        return { }


class AboutPage(BasePage):
    
    def _get_values(self):
        return { }
