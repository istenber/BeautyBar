from model.data import Item, Data
from model.generator_factory import GeneratorFactory
from ui.basepage import BasePage


class MainPage(BasePage):
    
    def _get_values(self):
        return { 'complex'    : True }

