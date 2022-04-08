from manim import *
from manim.mobject.opengl_compatibility import ConvertToOpenGL
from manim.mobject.geometry import ArrowTriangleFilledTip


class ZCurveArrow(TipableVMobject, metaclass=ConvertToOpenGL):
    def __init__(self, start, end,
                 direction=RIGHT,
                 stroke_width=6,
                 buff=MED_SMALL_BUFF,
                 ratio=4 / 5,
                 max_tip_length_to_length_ratio=0.25,
                 max_stroke_width_to_length_ratio=5, **kwargs):
        super(ZCurveArrow, self).__init__(stroke_width=stroke_width, **kwargs)
        if direction[0] != 0:
            self.add_cubic_bezier_curve(start, [end[0] * ratio + start[0] * (1 - ratio), start[1], 0],
                                        [start[0] * ratio + end[0] * (1 - ratio), end[1], 0], end)
        else:
            self.add_cubic_bezier_curve(start, [start[0], end[1] * ratio + start[1] * (1 - ratio), 0],
                                        [end[0], start[1] * ratio + end[1] * (1 - ratio), 0], end)
        self.max_tip_length_to_length_ratio = max_tip_length_to_length_ratio
        self.max_stroke_width_to_length_ratio = max_stroke_width_to_length_ratio
        tip_shape = kwargs.pop("tip_shape", ArrowTriangleFilledTip)
        self.tip = ArrowTriangleFilledTip()
        self.initial_stroke_width = self.stroke_width
        self.add_tip(tip_shape=tip_shape)
        self.set_stroke_width_from_length()

    def scale(self, factor, scale_tips=False, **kwargs):
        r"""Scale an arrow, but keep stroke width and arrow tip size fixed.

        See Also
        --------
        :meth:`~.Mobject.scale`

        Examples
        --------
        ::

            >>> arrow = Arrow(np.array([-1, -1, 0]), np.array([1, 1, 0]), buff=0)
            >>> scaled_arrow = arrow.scale(2)
            >>> np.round(scaled_arrow.get_start_and_end(), 8) + 0
            array([[-2., -2.,  0.],
                   [ 2.,  2.,  0.]])
            >>> arrow.tip.length == scaled_arrow.tip.length
            True

        Manually scaling the object using the default method
        :meth:`~.Mobject.scale` does not have the same properties::

            >>> new_arrow = Arrow(np.array([-1, -1, 0]), np.array([1, 1, 0]), buff=0)
            >>> another_scaled_arrow = VMobject.scale(new_arrow, 2)
            >>> another_scaled_arrow.tip.length == arrow.tip.length
            False

        """
        if self.get_length() == 0:
            return self

        if scale_tips:
            super().scale(factor, **kwargs)
            self.set_stroke_width_from_length()
            return self

        has_tip = self.has_tip()
        has_start_tip = self.has_start_tip()
        if has_tip or has_start_tip:
            old_tips = self.pop_tips()

        super().scale(factor, **kwargs)
        self.set_stroke_width_from_length()

        if has_tip:
            self.add_tip(tip=old_tips[0])
        if has_start_tip:
            self.add_tip(tip=old_tips[1], at_start=True)
        return self

    def get_normal_vector(self) -> np.ndarray:
        """Returns the normal of a vector.

        Examples
        --------
        ::

            >>> np.round(Arrow().get_normal_vector()) + 0. # add 0. to avoid negative 0 in output
            array([ 0.,  0., -1.])
        """

        p0, p1, p2 = self.tip.get_start_anchors()[:3]
        return normalize(np.cross(p2 - p1, p1 - p0))

    def reset_normal_vector(self):
        """Resets the normal of a vector"""
        self.normal_vector = self.get_normal_vector()
        return self

    def get_default_tip_length(self) -> float:
        """Returns the default tip_length of the arrow.

        Examples
        --------

        ::

            >>> Arrow().get_default_tip_length()
            0.35
        """

        max_ratio = self.max_tip_length_to_length_ratio
        return min(self.tip_length, max_ratio * self.get_length())

    def set_stroke_width_from_length(self):
        """Used internally. Sets stroke width based on length."""
        max_ratio = self.max_stroke_width_to_length_ratio
        if config.renderer == "opengl":
            self.set_stroke(
                width=min(self.initial_stroke_width, max_ratio * self.get_length()),
                recurse=False,
            )
        else:
            self.set_stroke(
                width=min(self.initial_stroke_width, max_ratio * self.get_length()),
                family=False,
            )
        return self
