import logging
import random

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Title

from lib.svgfig import *


FIGURE_PATH = 'M 39.08866,901.5024 L 43.95708,879.71409 L 54.88733,873.57248 L 58.08736,857.11628 L 50.83599,858.83411 L 50.59276,871.73303 L 38.05869,876.7725 L 35.23111,881.68276 L 29.34032,881.68276 L 26.51274,876.7725 L 13.978673,871.73303 L 13.73544,858.83411 L 6.484073,857.11628 L 9.6841,873.57248 L 20.61436,879.71409 L 25.48284,901.5024 L 19.877132,919.6118 L 9.798188,923.4351 L 8.407202,927.6081 L 27.8658,925.1758 L 30.98982,898.0706 L 33.58176,898.0706 L 36.70578,925.1758 L 56.16438,927.6081 L 54.77338,923.4351 L 44.69444,919.6118 L 39.08866,901.5024 z'

FIGURE_NECK = 'M 27.185665,881.28515 L 29.019246,874.96948 L 35.742381,874.96948 L 37.983425,881.69261'

FIGURE_HEAD = [{ 'skin' : ['M 24.169924,866.28424 L 22.693312,867.61679 L 23.053461,870.42596 L 24.854208,872.08265', 'M 39.512294,865.20379 L 40.952894,866.75243 L 40.556729,869.8137 L 39.188159,871.2543', 'M 26.37074,861.72694 L 24.129693,865.39411 L 24.944621,872.93217 L 28.611784,879.6553 L 35.538649,879.6553 L 39.205815,872.93217 L 39.409545,864.37545 L 37.168501,861.11575 L 26.37074,861.72694 z', 'M 32.328017,864.92928 L 36.972535,864.07371', 'M 26.565474,864.64247 L 31.246306,865.00879', 'M 30.364496,869.38152 L 29.500137,872.6949 L 29.932316,873.73933 L 34.146066,872.65888'],
                'hair' : ['M 23.557671,866.21221 C 23.91782,866.06815 26.799015,862.39462 26.799015,862.39462 L 36.667114,861.74635 L 39.116129,864.91567 L 40.484696,864.2674 L 38.179742,859.22531 L 24.27797,860.30575 L 22.333162,865.41988 L 23.557671,866.21221 z'],
                'mouth' : ['M 28.095555,875.43204 L 29.824271,877.88105 L 35.874785,875.72015 L 36.126889,874.63971 L 28.095555,875.43204 z'],
                'eyew' : ['M 32.659495,866.21632 L 33.013048,868.02828 L 35.134368,869.00055 L 37.565048,867.67473 L 37.565048,865.99535 L 36.150834,865.11147 L 32.659495,866.21632 z', 'M 27.267805,866.17213 L 28.947184,865.42083 L 31.156893,866.30471 L 30.759145,868.11667 L 29.123961,868.73539 L 26.914252,867.54215 L 27.267805,866.17213 z'],
                'eyeb' : ['M 28.637825,865.99535 L 28.019106,867.1444 L 28.947184,868.16087 L 29.875262,867.27698 L 29.521708,866.43729 L 28.637825,865.99535 z', 'M 34.780815,866.01744 L 34.162096,867.16649 L 35.090174,868.18296 L 36.018252,867.29907 L 35.664698,866.45938 L 34.780815,866.01744 z']},

               {'skin' : ['M 27.125763,878.50632 L 38.53057,878.50632 L 38.24184,874.17538 L 40.407309,868.40082 L 38.097471,859.8833 L 32.755986,858.29529 L 26.115217,860.31639 L 24.094109,866.23534 L 25.970849,872.29865 L 27.125763,878.50632 z', 'M 30.734879,868.8339 L 30.013055,871.72119 L 31.456702,872.44301 L 34.343994,872.44301 L 35.932001,870.99938 L 34.343994,868.25645'],
                'mouth' : ['M 28.85814,874.17538 L 28.85814,877.06269 L 35.643279,876.91831 L 36.076371,873.30921 L 28.85814,874.17538 z'],
                'hair' : ['M 25.393394,874.17538 L 27.558864,873.88666 L 25.682117,867.53462 L 27.703225,861.61567 L 32.755986,860.31639 L 36.365101,860.46076 L 39.396755,867.53462 L 39.829847,873.02047 L 42.284047,871.86557 L 40.840401,860.02766 L 34.777085,855.84108 L 25.682117,858.58402 L 22.07301,865.36915 L 25.393394,874.17538 z'],
                'eyew' : ['M 33.33344,864.7917 C 33.189078,865.36915 33.622171,866.95715 33.622171,866.95715 L 36.076371,868.11208 L 38.097471,866.3797 L 37.375648,864.93606 L 33.33344,864.7917 z', 'M 27.125763,867.53462 L 28.85814,868.25645 L 31.889794,867.10153 L 31.60107,864.64734 L 28.425049,865.22479 L 27.125763,867.53462 z'],
                'eyeb' : ['M 35.46875,865.17468 L 34.78125,866.17468 L 35.34375,867.29968 L 36.84375,866.61218 L 35.46875,865.17468 z', 'M 29.1875,865.54968 L 28.5,866.54968 L 29.0625,867.67468 L 30.5625,866.98718 L 29.1875,865.54968 z']},

               {'skin' : ['M 36.966969,862.24415 C 37.11133,862.60506 38.554976,864.19308 38.554976,864.19308 L 37.760969,865.13145', 'M 26.500531,864.4818 L 25.562162,866.71945 L 26.789261,867.22473', 'M 28.088546,871.05038 L 29.0991,877.69118 L 30.975839,878.70172 L 33.574399,878.99045 L 35.306777,877.69118 L 35.88423,876.82497 L 37.039146,870.47294 L 37.760969,865.56454 L 35.739869,858.3463 L 31.553292,856.3252 L 28.377277,857.04703 L 26.067438,861.52234 L 26.789261,867.73001 L 28.088546,871.05038 z', 'M 31.408931,867.44127 L 30.975839,870.11202 L 33.430031,869.96766 L 34.440584,868.45183'],
                'mouth' : ['M 30.109646,873.14366 L 30.398377,876.89717 L 32.852577,877.90771 L 34.945862,875.38132 L 34.873678,871.70003 L 30.109646,873.14366 z'],
                'hair' : ['M 26.35617,859.28468 L 34.65713,856.54176 L 33.430031,854.30411 L 27.294539,856.03648 L 26.35617,859.28468 z'],
                'eyew' : ['M 28.377277,864.26527 L 30.831469,865.56454 L 32.419477,863.97653 L 30.687108,861.81106 L 28.377277,864.26527 z', 'M 33.28567,864.26527 L 34.584954,865.99764 L 36.461692,864.1209 L 35.018046,861.37797 L 33.28567,864.26527 z'],
                'eyeb' : ['M 34.375,862.86218 L 34.1875,864.42468 L 34.9375,864.98718 L 35.8125,864.11218 L 35.25,863.04968 L 34.375,862.86218 z', 'M 30.0625,862.79968 L 29.875,864.36218 L 30.625,864.92468 L 31.5,864.04968 L 30.9375,862.98718 L 30.0625,862.79968 z']},

               {'skin' : ['M 27.354211,876.07039 L 31.135711,879.04974 L 34.917221,878.93514 L 35.833951,876.64333 L 39.157091,873.43478 L 42.480231,872.63265 L 41.334321,866.67391 L 38.125771,861.86108 L 33.198361,861.28813 L 29.646031,864.2675 L 27.812581,867.59064 L 29.302261,869.19492 L 27.927171,872.51805 L 27.354211,876.07039 z', 'M 33.312951,868.1636 C 32.625401,868.62196 31.937851,870.79919 31.937851,870.79919 L 33.312951,871.83051 L 35.719361,870.79919'],
                'mouth' : ['M 29.531451,874.12234 L 31.135711,877.33088 L 33.885911,876.64333 L 35.833951,874.5807 L 29.531451,874.12234 z'],
                'hair' : ['M 29.646031,863.007 L 32.167041,863.80914 L 34.115081,862.43404 L 38.584141,863.46537 L 40.875951,868.27819 L 41.448911,871.48673 L 42.365641,873.66397 L 43.969921,872.51805 L 42.594821,865.75719 L 38.240371,860.71518 L 31.594091,859.91304 L 29.646031,863.007 z'],
                'eyew' : ['M 33.198361,865.06964 L 32.167041,866.33014 L 34.115081,867.36146 L 35.490171,866.44473 L 33.198361,865.06964 z', 'M 37.552821,865.87178 L 36.063131,867.36146 L 37.209041,868.62196 L 39.271681,868.1636 L 37.552821,865.87178 z'],
                'eyeb' : ['M 33.410795,865.68599 L 33.057242,866.48149 L 33.587572,866.74665 L 34.294679,866.30471 L 33.410795,865.68599 z', 'M 37.388271,866.92343 L 37.034718,867.71893 L 37.565048,867.98409 L 38.272155,867.54215 L 37.388271,866.92343 z']},

               {'skin' : ['M 26.369959,877.80837 L 30.412168,878.96328 L 35.392745,879.25203 L 39.146233,877.37528 L 41.600417,869.94049 L 38.207847,864.81555 L 31.206175,863.805 L 25.070683,866.18701 L 24.132315,871.74506 L 26.369959,877.80837 z', 'M 33.876918,872.25033 L 36.54767,874.34362 L 32.433272,874.12707'],
                'mouth' : ['M 29.762529,875.85945 L 33.588189,877.95274 L 37.558208,875.93163 L 29.762529,875.85945 z'],
                'hair' : ['M 24.421035,867.9194 L 26.730878,866.6923 L 30.845257,864.74337 L 37.846946,865.32084 L 40.589867,869.29086 L 41.744787,869.29086 L 38.929683,863.94937 L 30.195618,862.5779 L 24.060126,865.24864 L 23.554856,868.20814 L 24.421035,867.9194 z'],
                'eyew' : ['M 27.380516,869.94049 L 31.278356,872.68343 L 33.082911,870.8067 L 27.380516,869.94049 z', 'M 34.670926,870.8067 L 36.114562,872.46687 L 40.301147,870.51795 L 34.670926,870.8067 z'],
                'eyeb' : ['M 30.228815,871.07768 L 31.02431,871.96156 L 31.55464,871.34285 L 31.377863,870.98929 L 30.228815,871.07768 z', 'M 35.753087,871.12188 L 36.548582,872.00576 L 37.078912,871.38705 L 36.902135,871.03349 L 35.753087,871.12188 z']},

               {'skin' : ['M 37.260269,863.13916 C 38.270829,863.71661 37.837729,864.5828 38.415189,864.43844 C 38.992649,864.29408 40.436289,862.85043 40.436289,862.85043 L 39.136999,860.68496', 'M 22.968179,861.55114 L 22.823809,864.43844 L 24.700549,865.59336 L 25.855469,864.29408', 'M 26.577339,871.90728 L 26.446199,876.95613 L 29.527949,879.51334 L 34.642389,880.10349 L 38.379849,876.56271 L 38.183129,872.16958 L 35.691489,870.3992 L 35.757059,865.28477 L 39.297829,860.62934 L 38.773269,856.36732 L 34.314539,854.59695 L 27.626439,854.66252 L 22.446459,857.08858 L 22.577599,860.89162 L 24.872539,863.57996 L 27.233019,865.0225 L 27.495309,869.15338 L 26.577339,871.90728 z', 'M 31.196959,862.27296 L 30.258579,867.75881 L 33.578979,867.25354'],
                'mouth' : ['M 27.876569,872.16194 L 28.165299,876.05978 L 31.918769,878.08089 L 36.538439,876.13197 L 35.455719,871.80103 L 27.876569,872.16194 z'],
                'hair' : ['M 21.813263,858.51949 L 27.299119,855.92093 L 34.661709,855.77657 L 38.126449,857.50894 L 40.003179,857.36458 L 38.559559,855.05474 L 30.330769,853.46673 L 23.401269,854.47729 L 20.225248,857.50894 L 21.813263,858.51949 z'],
                'eyew' : ['M 27.443479,858.23076 L 26.721649,860.5406 L 28.742769,862.12861 L 31.341329,859.6744 L 27.443479,858.23076 z', 'M 34.084249,857.79766 C 33.073699,858.37512 32.496239,860.39623 32.496239,860.39623 L 33.795519,862.56169 L 37.115909,861.11805 L 34.084249,857.79766 z'],
                'eyeb' : ['M 28.107495,859.5872 L 27.84233,860.55947 L 28.637825,861.35496 L 29.43332,860.20591 L 28.107495,859.5872 z', 'M 33.941126,859.76398 L 33.675961,860.73625 L 34.471456,861.53174 L 35.266951,860.38269 L 33.941126,859.76398 z']},

               {'skin' : ['M 27.011772,872.98497 C 27.011772,873.8016 29.461732,879.10983 29.461732,879.10983 L 34.157452,878.7015 L 37.832382,876.25155 L 38.853192,871.35167 L 37.015742,866.04344 L 33.340812,862.16436 L 28.032592,862.77683 L 25.786812,868.28922 L 27.011772,872.98497 z', 'M 31.299182,871.55581 L 30.482542,872.78079 L 31.095022,873.59743 L 32.728312,873.59743 L 33.544982,872.1683 L 32.728312,871.75997'],
                'mouth' : ['M 29.257572,875.02658 L 30.482542,876.45572 L 32.728312,877.06819 L 35.586602,875.63905 L 35.790752,874.20992 L 33.544982,875.02658 L 30.890872,875.02658 L 29.257572,875.02658 z'],
                'hair' : ['M 36.403252,874.82241 L 40.894812,874.4141 L 39.669852,868.69755 L 35.994932,860.73522 L 29.257572,859.71441 L 23.949332,863.18518 L 23.132702,873.18911 L 23.745192,876.04739 L 28.032592,875.84322 L 25.582632,868.90171 L 28.236772,862.57269 L 32.932492,862.57269 L 36.607422,867.06424 L 38.036562,870.53501 L 36.403252,874.82241 z'],
                'eyew' : ['M 34.157452,868.53422 L 32.524172,869.55503 L 32.524172,870.77999 L 35.994932,870.98416 L 37.015742,869.55503 L 34.157452,868.53422 z', 'M 29.053402,868.49338 L 27.828432,869.92252 L 29.053402,870.53501 L 31.503362,870.12667 L 31.503362,868.90171 L 29.053402,868.49338 z'],
                'eyeb' : ['M 29.344931,868.95636 L 28.90299,869.92863 L 29.610097,870.10541 L 30.405592,869.57508 L 29.344931,868.95636 z', 'M 34.250484,869.17733 L 33.808543,870.1496 L 34.51565,870.32638 L 35.311145,869.79605 L 34.250484,869.17733 z']},
               ]

MEDAL_LEFT = 'M 29.970044,886.533 C 29.255839,886.2949 24.494478,876.6531 24.494478,876.6531 L 22.589934,876.058 L 29.851011,887.4852'
MEDAL_RIGHT = 'M 34.373701,886.533 C 35.087906,886.2949 39.849266,876.6531 39.849266,876.6531 L 41.753811,876.058 L 34.492734,887.4852'
MEDAL_GOLD = 'M 30.042724,888.84034 L 30.794181,890.4685 L 31.921369,888.96559 L 31.420394,893.59957 L 33.549521,893.59957 L 32.923308,887.33743 L 30.042724,888.84034 z'
MEDAL_SILVER = 'M 30.164759,888.53499 L 30.72219,889.98431 L 32.728945,888.89732 L 32.728945,890.20728 L 30.610705,892.10255 L 30.053274,892.88295 L 34.512726,892.88295 L 34.401239,891.6566 L 32.283001,891.87958 L 33.955294,889.98431 L 33.843807,887.42013 L 30.164759,888.53499 z'
MEDAL_BRONZE = 'M 30.351633,888.4393 L 30.845019,889.77144 L 32.719893,888.93269 L 33.163942,890.06748 L 32.275844,890.65954 L 32.127828,891.35029 L 33.114603,891.59698 L 33.015925,892.58375 L 31.141054,892.09037 L 30.697006,892.87978 L 32.719893,893.71855 L 34.496087,892.87978 L 33.774461,890.95558 L 34.21851,888.73533 L 32.522538,887.20583 L 30.351633,888.4393 z'
MEDAL_BASE = 'M 36.75,890.61218 A 4.5,4.5 0 1 1 27.75,890.61218 A 4.5,4.5 0 1 1 36.75,890.61218 z'

# TODO: add heads
class Figure(object):

    def __init__(self, x, size, color, text, has_head=True):
        self.x = x
        self.size = size
        self.color = color
        self.text = text
        self.has_head = has_head

    def add_medal(self, medal):
        if medal in ['gold', 'silver', 'bronze']:
            self.medal = medal

    def get_medal(self, t):
        g = SVG("g")
        rs = "fill:#000000;stroke:#000000;stroke-width:1px;"
        if self.medal == 'gold':
            c = 'ffff00'
            v = MEDAL_GOLD
        elif self.medal == 'silver':
            c = 'cccccc'
            v = MEDAL_SILVER
        else:
            c = 'c87137'
            v = MEDAL_BRONZE
        ms = "fill:#" + c + ";stroke:#000000;stroke-width:1px;"
        g.append(SVG("path", d=MEDAL_LEFT, style=rs, transform=t))
        g.append(SVG("path", d=MEDAL_RIGHT, style=rs, transform=t))
        g.append(SVG("path", d=MEDAL_BASE, style=ms, transform=t))
        g.append(SVG("path", d=v, style=ms, transform=t))
        return g

    def get_skin_color(self):
        r = random.random()
        cm = [[0.5, "fill:#ffaaaa;stroke:#000000;stroke-width:0.3px;"],
             [0.75, "fill:#d7845f;stroke:#000000;stroke-width:0.3px;"],
             [1, "fill:#d45500;stroke:#000000;stroke-width:0.3px;"]]
        for c in cm:
            if r < c[0]:
                return c[1]

    def get_mouth_color(self):
        r = random.random()
        cm = [[0.75, "fill:#800000;stroke:#000000;stroke-width:0.3px;"],
             [1, "fill:#ff0000;stroke:#000000;stroke-width:0.3px;"]]
        for c in cm:
            if r < c[0]:
                return c[1]

    def get_hair_color(self):
        r = random.random()
        cm = [[0.5, "fill:#ffff00;stroke:#000000;stroke-width:0.3px;"],
             [0.75, "fill:#808000;stroke:#000000;stroke-width:0.3px;"],
             [1, "fill:#aa0000;stroke:#000000;stroke-width:0.3px;"]]
        for c in cm:
            if r < c[0]:
                return c[1]

    def get_head_style(self):
        return int(random.random() * len(FIGURE_HEAD))

    def help_line(self):
        return SVG("path",
                   d="M %d,0 L %d,200" % (self.x + 25, self.x + 25),
                   style="stroke-width:1px;stroke:#000000;")

    def get_head(self, t):
        g = SVG("g")
        parts = {'skin' : self.skin,
                 'hair' : self.get_hair_color(),
                 'mouth' : self.get_mouth_color(),
                 'eyew' : "fill:#ffffff;stroke:#000000;stroke-width:0.3px;",
                 'eyeb' : "fill:#0000ff;stroke:none;"}
        order = ['skin', 'mouth', 'eyew', 'eyeb', 'hair']
        head = self.get_head_style()
        for part in order:
            for path in FIGURE_HEAD[head][part]:
                g.append(SVG("path", d=path, style=parts[part], transform=t))
        return g

    def output(self):
        self.skin = self.get_skin_color()
        v = self.size
        # x = self.x - 6.2826161
        a = 0.4158 + 0.576 * v
        b = -2.696 - 3.75 * v + self.x + 14.2 - 15 * v
        c = -235.7 - 534 * v
        t = "matrix(%f,0,0,%f,%f,%f)" % (a, a, b, c)
        # + str(a) + 0.9689305,0,0,0.9689305," + str(x) + ",-748.78778)"
        figure = "fill:#" + self.color + ";"
        shadow = "fill:#000000;filter:url(#figure_shadow);"
        g = SVG("g")
        if self.has_head:
            g.append(SVG("path", d=FIGURE_NECK, style=self.skin, transform=t))
        g.append(SVG("path", d=FIGURE_PATH, style=shadow, transform=t))
        g.append(SVG("path", d=FIGURE_PATH, style=figure, transform=t))
        if hasattr(self, "medal"):
            g.append(self.get_medal(t))
        g.append(SVG("rect", x=12, width=40, y=830, height=30,
                     style="fill:#ffffff;stroke:#000000;stroke-width:1px;",
                     transform=t))
        g.append(Text(32, 850, self.text,
                      font_size=17,
                      transform=t,
                      style="fill:#000000;text-anchor:middle;").SVG())
        if self.has_head:
            g.append(self.get_head(t))
        # g.append(self.help_line())
        return g

    @classmethod
    def get_defs(cls):
        return SVG("filter", SVG("feGaussianBlur", stdDeviation=2),
                   id="figure_shadow")


class Champions(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.single_color = False
        self.color = "ffa733"
        self.has_medals = True
        self.has_grid = True
        self.has_head = True
        # TODO: more attributes

    def get_defs(self):
        return SVG("defs", Figure.get_defs())

    def get_elements(self):
        return SVG("g",
                   self.get_logo(),
                   self.get_meters(),
                   self.get_names(),
                   self.get_figures())

    def get_logo(self):
        g = SVG("g")
        g.append(SVG("circle", cx=128, cy=20, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=150, cy=20, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=172, cy=20, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=139, cy=31, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=161, cy=31, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        return g

    def get_names(self):
        g = SVG("g")
        for i in range(0, 6):
            x = 5 + i * 50
            g.append(SVG("rect", x=x, width=40, y=160, height=20,
                         style="fill:#ffffff;stroke:#000000;stroke-width:1px;"))
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x+20, 175, name, font_size=10,
                          style="fill:#000000;text-anchor:middle;").SVG())
        return g

    def get_meters(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=48, width=300, height=2,
                     style="fill:#888888;"))
        g.append(SVG("rect", x=0, y=50, width=300, height=2,
                     style="fill:#aaaaaa;"))
        if self.has_grid:
            for i in range(0, 4):
                g.append(SVG("rect", x=10, y=(118-i*10), width=280, height=2,
                             style="fill:#bbbbbb;"))
        g.append(SVG("rect", x=0, y=150, width=300, height=2,
                     style="fill:#aaaaaa;"))
        g.append(SVG("rect", x=0, y=152, width=300, height=2,
                     style="fill:#888888;"))
        return g

    def get_medalists(self):
        ordered = []
        for i in range(0, 6):
            ordered.append([i, self.get_row_value(i)])
        ordered.sort(cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)
        self.gold = ordered[0][0]
        self.silver = ordered[1][0]
        self.bronze = ordered[2][0]

    def get_figures(self):
        figs = SVG("g")
        colors = ['000080', '008000', '800000',
                  '808000', '008080', '800080']
        self.get_medalists()
        for i in range(0, 6):
            # 300 / 6 = 50
            if self.single_color:
                c = self.color
            else:
                c = colors[i]
            fig = Figure(x = i*50, color = c,
                         size = self.get_row_value(i),
                         text = self.get_row_value_str(i),
                         has_head = self.has_head)
            if self.has_medals:
                if self.gold == i:
                    fig.add_medal('gold')
                elif self.silver == i:
                    fig.add_medal('silver')
                elif self.bronze == i:
                    fig.add_medal('bronze')
            figs.append(fig.output())
        return figs

    def get_description(self):
        return "We are the champions"

    def get_ui_name(self):
        return "Champions"

    def get_attributes(self):
        has_medals = Boolean(self, "has_medals", "Medals for the champions")
        has_grid = Boolean(self, "has_grid", "Background grid")
        figure = Title(self, "Figures")
        single_color = Boolean(self, "single_color",
                               "All are same color")
        color = Color(self, "color", "Color")
        has_head = Boolean(self, "has_head", "With random heads")
        return [has_medals, has_grid, figure, single_color, color, has_head]

    def get_rating(self):
        return 3

    def get_version(self):
        return 1
