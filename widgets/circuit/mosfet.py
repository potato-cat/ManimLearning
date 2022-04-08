from manim import *
from widgets.scene import MScene
import os.path as path


class Mosfet(VMobject):
    def __init__(self, **kwargs):
        super(Mosfet, self).__init__(kwargs)
        # self.mosfet = SVGMobject(path.join(path.dirname(__file__), 'SVG/mosfet.svg'), color=BLACK, stroke_width=0.1,
        #                          height=8, fill_opacity=0, stroke_color=WHITE)
        self.mosfet = ImageMobject(path.join(path.dirname(__file__), 'SVG/mosfet.png'),
                                   scale_to_resolution=3000)\
            .scale_to_fit_height(config.frame_height).to_edge(LEFT)
        self.add(self.mosfet)


class TestScene(MScene):
    def construct(self):
        self.drawGrid()
        self.mosfet = Mosfet()
        self.add(self.mosfet)
        