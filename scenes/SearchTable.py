from manim import *
from scenes.my_ctex import my_ctex
from widgets.Struct import Struct
from widgets.ZCurveArrow import ZCurveArrow

SPACE = 1.5
WIDTH = 1
UNIT_HEIGHT = 0.25
FONT_SIZE = 20
RUN_TIME = 0.5
ARROW_LENGTH = 0.5


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.__next = None
        self.object = None
        self.line = None

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next):
        assert type(next) == Node
        self.__next = next


class SearchTable:
    def __init__(self, scene, statusRect=None, unitWidth=WIDTH, unitHeight=UNIT_HEIGHT, space=SPACE,
                 posX=-config.frame_x_radius, posY=-2, run_time=RUN_TIME):
        self.scene = scene
        self.unitWidth = unitWidth
        self.unitHeight = unitHeight
        self.space = space
        self.data = None
        self.posX = posX
        self.posY = posY
        self.pointer = None
        self.statusRect = statusRect
        self.status = None
        self.runTime = run_time

    def put(self, key, value):
        if self.status:
            self.scene.remove(self.status)
            self.status = None
        if self.data == None:
            struct_object = Struct('ST', {'key': key, 'val': value}, 'NULL', self.unitWidth, self.unitHeight, FONT_SIZE)
            node = Node(key, value)
            self.data = node
            node.object = struct_object.move_to([self.posX, self.posY, 0], LEFT + DOWN)
            node.line = None
            self.pointer = Arrow(start=node.object.get_critical_point(DOWN) - np.array([0, ARROW_LENGTH, 0]),
                                 end=node.object.get_critical_point(DOWN), buff=0, stroke_width=2, tip_length=0.1)
            self.scene.play(Create(node.object, run_time=self.runTime), Create(self.pointer))
        else:
            node = self.data
            self.pointer.move_to(node.object.get_critical_point(DOWN), UP)
            self.scene.wait(0.5)
            while node is not None:
                if key == node.key:  # 命中
                    struct_object = Struct('ST', {'key': key, 'val': value}, node.object.nextStr, self.unitWidth,
                                           self.unitHeight, FONT_SIZE)
                    node.value = value
                    struct_object = struct_object.move_to(node.object)
                    if self.statusRect:
                        self.scene.play(self.setStatus('命中'), *node.object.setColor(RED, self.runTime))
                    self.scene.wait(0.5)
                    self.scene.play(ReplacementTransform(node.object, struct_object, run_time=self.runTime))
                    node.object = struct_object
                    return
                else:
                    node = node.next
                    if node:
                        self.scene.play(
                            self.pointer.animate(run_time=self.runTime).move_to(node.object.get_critical_point(DOWN),
                                                                                UP))

            struct_object = Struct('ST', {'key': key, 'val': value}, 'prev', self.unitWidth, self.unitHeight, FONT_SIZE)
            node = Node(key, value)
            node.object = struct_object.move_to(
                self.data.object.get_critical_point(LEFT + DOWN) + np.array([self.space, 0, 0]),
                LEFT + DOWN)
            node.line = ZCurveArrow(node.object.getPrevPoint(), self.data.object.getCurPoint(),
                                    max_tip_length_to_length_ratio=0.1, stroke_width=2, tip_length=0.2)
            node.next = self.data
            if self.statusRect:
                self.scene.play(self.setStatus('未命中'))
            self.scene.play(Create(node.line, run_time=self.runTime))
            self.scene.play(Create(node.object, run_time=self.runTime))
            self.data = node
            self.pointer.move_to(node.object.get_critical_point(DOWN), UP)

    def get(self, key):
        if self.status:
            self.scene.remove(self.status)
            self.status = None
        if self.data == None:
            return None
        else:
            node = self.data
            self.pointer.move_to(node.object.get_critical_point(DOWN), UP)
            self.scene.wait(0.5)
            while node is not None:
                if key == node.key:  # 命中
                    if self.statusRect:
                        self.scene.play(self.setStatus('命中'), *node.object.setColor(RED, self.runTime))
                    self.scene.wait(0.5)
                    self.scene.play(*node.object.setColor(BLUE, self.runTime))
                    return node.value
                else:
                    node = node.next
                    if node:
                        self.scene.play(
                            self.pointer.animate(run_time=self.runTime).move_to(node.object.get_critical_point(DOWN),
                                                                                UP))
            return None

    def setStatus(self, status):
        oldStatus = self.status
        if oldStatus is None:
            self.status = Tex(status, tex_template=my_ctex(), font_size=FONT_SIZE).move_to(self.statusRect)
            return FadeIn(self.status, run_time=self.runTime)
        else:
            self.status = Tex(status, tex_template=my_ctex(), font_size=FONT_SIZE).move_to(self.statusRect)
            return ReplacementTransform(oldStatus, self.status, run_time=self.runTime)

    def clear(self):
        animations = []
        animations.append(Uncreate(self.pointer))
        if self.status:
            animations.append(Uncreate(self.status))
        node = self.data
        while node is not None:
            animations.append(Uncreate(node.object))
            if node.line:
                animations.append(Uncreate(node.line))
            node = node.next
        return animations
