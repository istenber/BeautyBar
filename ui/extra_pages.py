import logging

from ui.basepage import ExtraPage


MAX_COUNT = 20
POPULAR_IMAGES = None

# TODO: make common function with attributes/complex!!
def populars_from_db():
    global POPULAR_IMAGES
    if POPULAR_IMAGES is None:
        from ui.image import Image
        objs = Image.gql("WHERE role = :1", "popular").fetch(MAX_COUNT)
        POPULAR_IMAGES = sorted(map(lambda x: x.name.split("/")[1], objs))
    return POPULAR_IMAGES



class LearnPage(ExtraPage):
    
    def _is_valid_page(self, page):
        return page in ['basics', 'style']

    def get_values(self):
        page = self.request.get("page")
        if page != "" and self._is_valid_page(page):
            return { 'template' : "learn" + page }
        return { }


class AboutPage(ExtraPage):
    
    def get_values(self):
        return { }


# TODO:
# - make automatic image creation?
# - make popular page link from mainpage
# - give star ratings for populars
# - do paging and tablezing for populars
# - rethink dbimages naming?
class PopularPage(ExtraPage):

    def get_values(self):
        return { 'populars' : populars_from_db() }
