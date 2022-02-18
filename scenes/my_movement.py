from typing import Optional
from manim import *


class MyMoveAlongPath(Animation):
    """Make one mobject move along the path of another mobject.
    Example
    --------
    .. manim:: MoveAlongPathExample

        class MoveAlongPathExample(Scene):
            def construct(self):
                d1 = Dot().set_color(ORANGE)
                l1 = Line(LEFT, RIGHT)
                l2 = VMobject()
                self.add(d1, l1, l2)
                l2.add_updater(lambda x: x.become(Line(LEFT, d1.get_center()).set_color(ORANGE)))
                self.play(MoveAlongPath(d1, l1), rate_func=linear)
    """

    def __init__(
        self,
        mobject: "Mobject",
        path: "VMobject",
        suspend_mobject_updating: Optional[bool] = False,
        aligned_edge = ORIGIN,
        **kwargs
    ) -> None:
        self.path = path
        self.aligned_edge = aligned_edge
        super().__init__(
            mobject,  suspend_mobject_updating=suspend_mobject_updating, **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        point = self.path.point_from_proportion(self.rate_func(alpha))
        self.mobject.move_to(point, aligned_edge=self.aligned_edge)