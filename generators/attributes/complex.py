from attribute import Attribute
from ui.image import Image


MAX_COUNT = 20


class Background(Attribute):
    def choices(self):
        # TODO: we should precalc this!
        choices = Image.gql("WHERE role = :1", "attribute").fetch(MAX_COUNT)
        return sorted(map(lambda x: x.name.split("/")[1], choices))
