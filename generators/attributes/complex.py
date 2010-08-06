from attribute import Attribute
import logging


MAX_COUNT = 20
BACKGROUND_IMAGES = None


# TODO: make general caching function
# TODO: make admin function to reload this automatically?
# TODO: max count needs to be larger
def choices_from_db(force_reload=False):
    global BACKGROUND_IMAGES
    if (BACKGROUND_IMAGES is None) or force_reload:
        from ui.image import Image
        objs = Image.gql("WHERE role = :1", "attribute").fetch(MAX_COUNT)
        BACKGROUND_IMAGES = sorted(map(lambda x: x.name.split("/")[1], objs))
    return BACKGROUND_IMAGES


class Background(Attribute):
    def choices(self):
        return choices_from_db()
