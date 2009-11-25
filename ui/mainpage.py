from model.data import Item, Data
from model.generator_factory import GeneratorFactory
from ui.basepage import ActivePage


class MainPage(ActivePage):
    
    def get_values(self):
        return { 'complex'    : True }

