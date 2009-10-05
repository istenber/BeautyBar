from google.appengine.ext import db
from model.data import Item, Data

class ItemDAO(db.Model):
    name     = db.StringProperty(required=True)
    value    = db.StringProperty(required=True)
    data_ref = db.StringProperty(required=True)

    @staticmethod
    def save(ref, item):
        dao = ItemDAO(name     = str(item.name),
                      value    = str(item.value),
                      data_ref = str(ref))
        dao.put()

class DataDAO(db.Model):
    name       = db.StringProperty(required=True)
    
    @staticmethod
    def load(name):
        data = Data()
        items = db.GqlQuery("SELECT * FROM ItemDAO WHERE data_ref = :1",
                            name)
        for item in items:
            data.add_item(Item(item.name, item.value))
        return data
    
    @staticmethod
    def save(data, name):
        dao = DataDAO(name = str(name))
        for item in data.items:
            ItemDAO.save(name, item)
        dao.put()
