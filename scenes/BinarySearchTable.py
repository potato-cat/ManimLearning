from manim import *
from widgets.Struct import Struct

INTERVAL = 0.25
WIDTH = 0.5
SPACE = INTERVAL + WIDTH
UNIT_HEIGHT = 0.25
FONT_SIZE = 20
RUN_TIME = 0.5
ARROW_LENGTH = 0.5


class BinarySearchTable:
    def __init__(self, scene, capacity, posX=-config.frame_x_radius + INTERVAL, posY=-2):
        self.scene = scene
        self.capacity = capacity
        self.posX = posX
        self.posY = posY

        self.keys = []
        self.values = []
        self.objs = []

        self.rect = Rectangle(width=self.capacity * SPACE, height=3 * UNIT_HEIGHT + 0.2).move_to(
            [self.posX - INTERVAL / 2, self.posY, 0], LEFT)
        self.pointer = None
        self.lpointer = None
        self.hpointer = None

    def clearScene(self):
        animations = [Uncreate(self.rect, run_time=RUN_TIME), Uncreate(self.pointer, run_time=RUN_TIME)]
        for obj in self.objs:
            animations.append(Uncreate(obj, run_time=RUN_TIME))
        return animations

    def initScene(self, run_time=RUN_TIME):
        self.scene.play(Create(self.rect, run_time=run_time))

    def put(self, key, value):
        if len(self.keys) == 0 or key > self.keys[-1]:
            self.objs.append(Struct('BST', {'key': key, 'val': value}, unitWidth=WIDTH, unitHeight=UNIT_HEIGHT) \
                             .move_to([self.posX + len(self.keys) * SPACE, self.posY, 0], LEFT))
            self.keys.append(key)
            self.values.append(value)
            self.scene.play(Create(self.objs[-1], run_time=RUN_TIME))
        else:
            rank = self.rank(key)
            if rank < len(self.keys) and key == self.keys[rank]:
                oldobj = self.objs[rank]
                self.objs[rank] = Struct('BST', {'key': key, 'val': value}, unitWidth=WIDTH, unitHeight=UNIT_HEIGHT) \
                    .move_to(oldobj)
                self.keys[rank] = key
                self.values[rank] = value
                self.scene.play(*oldobj.setColor(RED))
                self.scene.wait(0.5)
                self.scene.play(ReplacementTransform(oldobj, self.objs[rank], run_time=RUN_TIME))
            else:
                obj = self.objs[rank]
                self.scene.play(*obj.setColor(RED))
                self.keys.append(key)
                self.values.append(value)
                self.objs.append(Struct('BST', {'key': key, 'val': value}, unitWidth=WIDTH, unitHeight=UNIT_HEIGHT))
                animations = []
                for i in range(len(self.keys) - 2, rank - 1, -1):
                    self.keys[i + 1] = self.keys[i]
                    self.values[i + 1] = self.values[i]
                    self.objs[i + 1] = self.objs[i]
                    animations.append(self.objs[i].animate(run_time=RUN_TIME).shift([SPACE, 0, 0]))
                if animations:
                    self.scene.play(*animations)
                self.keys[rank] = key
                self.values[rank] = value
                self.objs[rank] = Struct('BST', {'key': key, 'val': value}, unitWidth=WIDTH, unitHeight=UNIT_HEIGHT) \
                    .move_to([self.posX + SPACE * rank, self.posY, 0], LEFT)
                self.scene.play(Create(self.objs[rank], run_time=RUN_TIME), *obj.setColor(BLUE, RUN_TIME))

    def delete(self, key):
        if len(self.keys) == 0:
            return
        else:
            rank = self.rank(key)
            if rank < len(self.keys) and key == self.keys[rank]:
                oldobj = self.objs[rank]
                self.scene.play(*oldobj.setColor(RED))
                animations = []
                for i in range(rank, len(self.keys)-1):
                    self.keys[i] = self.keys[i+1]
                    self.values[i] = self.values[i+1]
                    self.objs[i] = self.objs[i+1]
                    animations.append(self.objs[i+1].animate(run_time=RUN_TIME).shift([-SPACE, 0, 0]))
                self.scene.play(FadeOut(oldobj, run_time=RUN_TIME))
                if animations:
                    self.scene.play(*animations)
                self.keys.pop(-1)
                self.objs.pop(-1)
                self.values.pop(-1)
            else:
                return

    def rank(self, key):
        if len(self.keys) == 0:
            return 0
        low = 0
        high = len(self.keys) - 1
        self.scene.wait(0.5)
        self.lpointer = self.generateLRPointer(LEFT, 'L').move_to(
            [self.posX + low * SPACE + WIDTH / 2, self.objs[0].get_critical_point(DOWN)[1] - SMALL_BUFF, 0], UP + RIGHT)
        self.rpointer = self.generateLRPointer(RIGHT, 'H').move_to(
            [self.posX + high * SPACE + WIDTH / 2, self.objs[0].get_critical_point(DOWN)[1] - SMALL_BUFF, 0], UP + LEFT)
        self.scene.play(FadeIn(self.lpointer, run_time=RUN_TIME), FadeIn(self.rpointer, run_time=RUN_TIME))
        while low <= high:
            mid = (low + high) // 2
            if self.pointer == None:
                self.pointer = self.generatePointer().move_to(
                    self.objs[mid].get_critical_point(UP) + [0, SMALL_BUFF, 0], DOWN)
                self.scene.play(Create(self.pointer, run_time=RUN_TIME))
            else:
                self.scene.play(self.pointer.animate(run_time=RUN_TIME).move_to(
                    self.objs[mid].get_critical_point(UP) + [0, SMALL_BUFF, 0], DOWN))
            if self.keys[mid] == key:
                self.scene.play(FadeOut(self.lpointer, run_time=RUN_TIME),
                                FadeOut(self.rpointer, run_time=RUN_TIME))
                self.lpointer = None
                self.rpointer = None
                return mid
            if self.keys[mid] > key:
                high = mid - 1
            else:
                low = mid + 1
            if low > high:
                self.lpointer[0].set_color(RED)
                self.rpointer[0].set_color(RED)
            self.scene.play(
                self.lpointer.animate(run_time=RUN_TIME).move_to(
                    [self.posX + low * SPACE + WIDTH / 2, self.objs[0].get_critical_point(DOWN)[1] - SMALL_BUFF, 0],
                    UP + RIGHT),
                self.rpointer.animate(run_time=RUN_TIME).move_to(
                    [self.posX + high * SPACE + WIDTH / 2, self.objs[0].get_critical_point(DOWN)[1] - SMALL_BUFF, 0],
                    UP + LEFT))
        self.scene.play(FadeOut(self.lpointer, run_time=RUN_TIME),
                        FadeOut(self.rpointer, run_time=RUN_TIME))
        self.lpointer = None
        self.rpointer = None
        return low

    def generatePointer(self):
        return Triangle(color=PINK, stroke_width=2).rotate(PI).scale(0.1)

    def generateLRPointer(self, direction, text='L', scale=0.2):
        if direction[0] == -1:
            pointer = VGroup()
            polygon = Polygon([0, 0, 0], [0, -2, 0], [1, -2, 0], [1, -1, 0],
                              fill_opacity=0, fill_color=WHITE, stroke_color=WHITE, stroke_width=2) \
                .flip() \
                .scale(scale)
            text = Text(text, font_size=18, fill_color=WHITE, fill_opacity=1) \
                .move_to(polygon.get_critical_point(DOWN), aligned_edge=DOWN)
            pointer.add(polygon, text)
            return pointer
        else:
            pointer = VGroup()
            polygon = Polygon([0, 0, 0], [0, -2, 0], [1, -2, 0], [1, -1, 0],
                              fill_opacity=0, fill_color=WHITE, stroke_color=WHITE, stroke_width=2) \
                .scale(scale)
            text = Text(text, font_size=18, fill_color=WHITE, fill_opacity=1) \
                .move_to(polygon.get_critical_point(DOWN), aligned_edge=DOWN)
            pointer.add(polygon, text)
            return pointer
