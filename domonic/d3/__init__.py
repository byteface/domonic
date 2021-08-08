"""
    domonic.d3
    ====================================

"""

from domonic.html import *


# from.domonic.d3.format import *
# from.domonic.d3.queue import *
# from.domonic.d3.array import *
# from.domonic.d3.axis import *
# from.domonic.d3.brush import *
# from.domonic.d3.chord import *
# from.domonic.d3.color import *
# from.domonic.d3.contour import *
# from.domonic.d3.delaunay import *
# from.domonic.d3.dispatch import *
# from.domonic.d3.drag import *
# from.domonic.d3.dsv import *
# from.domonic.d3.ease import *
# from.domonic.d3.fetch import *
# from.domonic.d3.force import *
# from.domonic.d3.format import *
# from.domonic.d3.geo import *
# from.domonic.d3.heirarchy import *
# from.domonic.d3.interpolate import *
# from.domonic.d3.path import *
# from.domonic.d3.polygon import *
# from.domonic.d3.quadtree import *
# from.domonic.d3.queue import *
# from.domonic.d3.random import *
# from.domonic.d3.scale-chromatic import *
# from.domonic.d3.scale import *
from domonic.d3.selection import *
# from.domonic.d3.shape import *
# from.domonic.d3.tile import *
# from.domonic.d3.time-format import *
# from.domonic.d3.time import *
# from.domonic.d3.timer import *
# from.domonic.d3.transition import *
# from.domonic.d3.zoom import *







class d3_el():
    """
    d3_el - contains the d3_el class and its methods
    """

    DOM = None

    def __init__(self, dom, *args, **kwargs):
        if type(dom) == str:
            raise ValueError('d3_el.__init__: dom must be a DOM object')
        else:
            d3_el.DOM = dom
            self.dom = dom

    def __str__(self):
        return str(self.dom)

    @property
    def dom(self):
        if d3_el.DOM is None:
            raise ValueError('d3_el.dom: DOM has not been set')
        return d3_el.DOM

    @dom.setter
    def dom(self, dom):
        if isinstance(dom, html) or isinstance(dom, Document):
            d3_el.DOM = dom

    def init(self, q=''):
        self.q = q
        if type(q) is not str:
            return
        # if q == "":
            # return

        if self.q[0] == '<':
            self.elements = domonic.domonic.load(self.q)
            if isinstance(self.elements, html) or isinstance(self.elements, Document):
                self.dom = self.elements
        else:
            try:
                # element by selector not working on just classes as always needs a tag
                if self.q[0] == '.':
                    self.elements = self.dom.querySelectorAll(self.q)
                    return
                self.elements = self.dom.getElementsBySelector(self.q, self.dom)
            except Exception as e:
                print('Error. No DOM has been set!!', e)
                raise e


def dproxy(q):
    el = d3_el(q)
    el.init(q)

    # if type(q) is not str:
    return el
    # else:
    #     return el.elements
    # def __str__(self):
    #     return self.elements


class d3(d3_el):

    def __init__(self, selector=None, *args, **kwargs):
        super().__init__(selector, *args, **kwargs)
        self.init(selector)

    def __call__(self, *args, **kwargs):
        return dproxy(args[0])