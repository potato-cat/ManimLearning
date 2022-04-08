from manim import *


class MScene(Scene):
    def drawGrid(self):
        plane = NumberPlane(axis_config={"include_numbers": True, 'stroke_width': 1, 'stroke_opacity': 0.5},
                            background_line_style={'stroke_opacity': 0.3})
        self.add(plane)

