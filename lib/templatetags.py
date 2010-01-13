import os

from google.appengine.ext import webapp
from django.template import Node, NodeList, Template # , Context, Variable

register = webapp.template.create_template_register()

# context copied from django/template/defaulttags.py
# app engine tags are made according:
#   http://daily.profeth.de/2008/04/using-custom-django-template-helpers.html

class IfStrEqualNode(Node):
    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfEqualNode>"

    def render(self, context):
        val1 = self.var1.resolve(context, True)
        val2 = self.var2.resolve(context, True)
        if ((self.negate and str(val1) != str(val2)) or
            (not self.negate and str(val1) == str(val2))):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_ifstrequal(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r takes two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    val1 = parser.compile_filter(bits[1])
    val2 = parser.compile_filter(bits[2])
    return IfStrEqualNode(val1, val2, nodelist_true, nodelist_false, negate)

#@register.tag
def ifstrequal(parser, token):
    """
    Outputs the contents of the block if the two arguments equal each other
    after str(). e. g. str(\"2\") == str(2) is True.

    Examples::

        {% ifstrequal user.id comment.user_id %}
            ...
        {% endifstrequal %}
    """
    return do_ifstrequal(parser, token, False)
ifstrequal = register.tag(ifstrequal)
