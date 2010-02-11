from model.generator_factory import GeneratorFactory
from ui.basepage import Page


class MainPage(Page):
    
    def get_values(self):
        return { 'complex'        : True,
                 'use_javascript' : True,
                 'generators'     : GeneratorFactory().rated_list(),
                 }
