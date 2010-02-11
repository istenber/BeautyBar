from model.generator_factory import GeneratorFactory
from ui.basepage import SessionPage, Page


class MainPage(Page, SessionPage):
    
    def get_values(self):
        # note: we need this here otherwise all ajax parts (might)
        #       generate own sessions
        self.get_session()
        return { 'complex'        : True,
                 'use_javascript' : True,
                 'generators'     : GeneratorFactory().rated_list(),
                 }
