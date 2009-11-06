from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO
from model.generator_factory import GeneratorFactory
from ui.basepage import BasePage

class MainPage(BasePage):
    
    def _get_values(self):
        data = DataDAO.load(self.session)
        items = data.as_list()
        # debug = "( data:" + str(data.as_list()) + " )"
        debug = "( session:" + str(self.session) + " )"
        # debug = "(" + str(dir(self.response)) + ")"
        values = {
            'items'      : items,
            'generators' : GeneratorFactory().list(),
            'debug'      : debug,
            'cur_gen'    : "bars",
            }
        return values

