from attribute import Attribute
import logging


MAX_COUNT = 20
BACKGROUND_IMAGES = None


def choices_from_db():
    global BACKGROUND_IMAGES
    if BACKGROUND_IMAGES is None:
        from ui.image import Image
        objs = Image.gql("WHERE role = :1", "attribute").fetch(MAX_COUNT)
        BACKGROUND_IMAGES = sorted(map(lambda x: x.name.split("/")[1], objs))
    return BACKGROUND_IMAGES


class Background(Attribute):
    def choices(self):
        return choices_from_db()
