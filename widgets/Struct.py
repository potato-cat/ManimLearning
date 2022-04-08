from manim import *
from scenes.my_ctex import my_ctex


class Struct(VGroup):
    def __init__(self, name, data, unitWidth=1, unitHeight=0.5, fontSize=20, **kwargs):
        super(Struct, self).__init__(**kwargs)
        self.struct = data
        self.fontSize = fontSize
        self.unitWidth = unitWidth
        self.unitHeight = unitHeight
        self.nameObject = self.createField(name, BLUE, **kwargs)
        self.add(self.nameObject)
        self.childs = []
        for i, k in enumerate(data):
            field = self.createField(data[k], BLUE, **kwargs)
            if i == 0:
                field.next_to(self.nameObject, DOWN, buff=0)
            else:
                field.next_to(self.childs[-1], DOWN, buff=0)
            self.childs.append(field)
            self.add(field)

    def createField(self, fieldName, color, **kwargs):
        field = VMobject()
        rect = Rectangle(color, self.unitHeight, self.unitWidth, **kwargs)
        text = Tex(str(fieldName), tex_template=my_ctex(), font_size=self.fontSize).move_to(rect)
        field.add(rect, text)
        return field

    def getLastPoint(self, direction=LEFT):
        return self.childs[-1].get_critical_point(direction)

    def getNamePoint(self, direction=RIGHT):
        return self.nameObject.get_critical_point(direction)

    def setColor(self, color, run_time=0.2):
        animations = []
        animations.append(self.nameObject[0].animate(run_time=run_time).set_color(color))
        for obj in self.childs:
            animations.append(obj[0].animate(run_time=run_time).set_color(color))
        return animations
