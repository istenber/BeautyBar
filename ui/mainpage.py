from model.data import Item, Data
from model.generator_factory import GeneratorFactory
from ui.basepage import BasePage

class MainPage(BasePage):
    
    def _get_values(self):
        items = self.session.data.as_list()
        cur_gen = self.session.style.get_active_generator()
        values = {
            'items'      : items,
            'generators' : GeneratorFactory().list(),
            'cur_gen'    : cur_gen,
            'r_min'      : self.session.data.min,
            'r_max'      : self.session.data.max,
            'complex'    : True,
            }
        return values

