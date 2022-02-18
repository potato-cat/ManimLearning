from my_movement import MyMoveAlongPath
from manim import *
import numpy as np

CARD_WIDTH = 0.5
CARD_SPACE = 1
CARD_MAX_HEIGHT = 2
CARD_MIN_HEIGHT = 0.5


class QuickSortScene(Scene):
    def construct(self):
        # 原点
        # origin = Dot()
        # self.add(origin)
        # 待排序数组
        self.arr = [11, 22, 33, 33, 55, 66, 77, 88, 99]
        self.cards = []
        self.cardGroup = VGroup()
        self.treeGroup = VGroup()
        self.group1 = VGroup()
        self.legendGroup = VGroup()
        self.currentStep = None

        title = Tex('快速排序',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft').to_edge(UP)
        self.add(title)

        introduction = Tex(
            '快速排序是一种基于分而治之思想实现的排序算法，它具有排序效率高、消耗资源少、容易实现等优点，'
            '是很多实际场景的首选排序算法。',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft').scale(0.6).next_to(title, DOWN).to_edge(LEFT)
        self.group1.add(introduction)
        self.play(Write(introduction))
        self.wait(1)
        implement = Tex(
            '快速排序实现时，通过递归地不断将数组分为小于某一个值（基准）的部分以及大于该值的部分，分别置于基准的左侧（右侧）'
            '以及右侧（左侧），直到不可分为止。',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft').scale(0.6).next_to(introduction, DOWN).to_edge(LEFT)
        self.group1.add(implement)
        self.play(Write(implement))
        self.wait(1)
        note1 = Tex('以升序排列为例，每一次分割，选择某个值为基准后，都需要左右两个指针来对分割区域进行遍历，'
                    '左指针不断右移寻找大于基准值的值，右指针不断左移寻找小于基准值的值，找到后将两个值进行调换，'
                    '直到两个指针相遇或者左指针右移到极限为止，此时，将左指针的值与基准进行调换，从而完成一轮分割。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft').scale(0.6).next_to(implement, DOWN).to_edge(LEFT)
        self.group1.add(note1)
        self.play(Write(note1, run_time=4))
        self.wait(1)
        self.arr = [11, 88, 77, 22, 33, 66, 99, 33, 55]
        self.setArray(self.arr, 33, -config.frame_y_radius+1)
        self.play(Write(self.cardGroup, run_time=3))
        self.showLegend(config.frame_y_radius+0.5)
        self.pointer1 = self.getPointer(0)
        self.pointer2 = self.getPointer(1)
        self.play(Write(self.pointer1), Write(self.pointer2))
        self.brace = self.getBrace(0, -1)
        self.play(Write(self.brace))
        self.split(0, len(self.arr) - 1)
        self.wait(3)

        self.play(Uncreate(self.brace), Uncreate(self.pointer1), Uncreate(self.pointer2),
                  Uncreate(self.cardGroup), Uncreate(self.group1), Uncreate(self.legendGroup))
        self.cards.clear()
        self.cardGroup = VGroup()
        self.group1 = VGroup()
        note2 = Tex('每一次遍历的终点条件应设为左指针位置大于等于右指针位置，因为当左侧所有的值都小于基准值时，'
                    '实际上并不需要调换指针所在值与基准，此时，只需要将左指针不断右移到基准处，最终对左指针所在值（基准）'
                    '与基准进行调换（即不调换），其他情况，均为左右指针相遇，此时，指针左侧数值均小于等于基准，右侧均大于等于基准，'
                    '基准调换到指针位置即完成左侧与右侧的分割，显然，此时基准数值在排序后数组中的位置已经确定。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft').scale(0.6).next_to(title, DOWN).to_edge(LEFT)
        self.group1.add(note2)
        self.play(Write(note2, run_time=5))

        self.wait(1)
        self.arr = [22, 11, 77, 33, 33, 66, 55, 88, 99]
        self.setArray(self.arr, 33, -config.frame_y_radius + 1)
        self.play(Write(self.cardGroup, run_time=3))
        self.showLegend(config.frame_y_radius+0.5)
        self.pointer1 = self.getPointer(0)
        self.pointer2 = self.getPointer(1)
        self.play(Write(self.pointer1), Write(self.pointer2))
        self.brace = self.getBrace(0, -1)
        self.play(Write(self.brace))
        self.split(0, len(self.arr) - 1)

        note3 = Tex('随后，分别对左右两部分重复这样的分割，每次都可以确定基准的位置，直到分无可分，算法结束，排序完成，'
                    '可以证明，快速排序的平均时间复杂度与最优时间复杂度均为$n\\text{log}n$，最差时间复杂度为$n^2$。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft').scale(0.6).next_to(note2, DOWN).to_edge(LEFT)
        self.group1.add(note3)
        self.play(Write(note3))

        self.wait(3)
        self.clear()

        self.cards = []
        self.cardGroup = VGroup()
        self.treeGroup = VGroup()
        self.legendGroup = VGroup()

        # np.random.shuffle(self.arr)
        self.arr = [11, 88, 77, 22, 33, 66, 99, 33, 55]
        self.setArray(self.arr, 33)
        self.play(Write(self.cardGroup, run_time=3))
        self.brace = self.getBrace(0, -1)
        self.play(Write(self.brace))
        self.pointer1 = self.getPointer(0)
        self.pointer2 = self.getPointer(1)
        self.play(Write(self.pointer1), Write(self.pointer2))
        tree0 = MathTex('[%s\\quad%s]' % (0, len(self.arr) - 1), stroke_width=2).scale(0.5)
        tree0.move_to([0, -tree0.height, 0])
        self.play(Write(tree0))
        self.showLegend()
        self.quickSort(0, len(self.arr) - 1, tree0, 1)
        self.wait(2)

        self.clear()
        self.add(title)
        note4 = Tex('快速排序是一种不稳定的排序算法，因为相同的值位于基准值两侧时，会在沿基准值分割时发生位置的交换，'
                    '从而改变相同值的位置顺序。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft').scale(0.6).next_to(title, DOWN).to_edge(LEFT)
        self.group1.add(note4)
        self.play(Write(note4))
        self.cards.clear()
        self.cardGroup = VGroup()
        self.arr = [11, 88, 77, 22, 33, 66, 99, 33, 55]
        self.setArray(self.arr, 33, -config.frame_y_radius + 1.5)
        self.play(Write(self.cardGroup, run_time=3))
        self.showLegend(config.frame_y_radius)
        self.pointer1 = self.getPointer(0)
        self.pointer2 = self.getPointer(1)
        self.play(Write(self.pointer1), Write(self.pointer2))
        self.brace = self.getBrace(0, -1)
        self.play(Write(self.brace))
        self.split(0, len(self.arr) - 1)
        self.wait(3)

    def showLegend(self, buff=1):
        self.legendGroup = VGroup()
        arrRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5,
                                   fill_color=BLUE, fill_opacity=1)
        arrLabel = Text('未排序数组', font_size=15).next_to(arrRect, RIGHT)
        arrLegend = VGroup(arrRect, arrLabel).to_edge(RIGHT, buff=0).to_edge(UP, buff=buff)

        pivotRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5,
                                   fill_color=RED, fill_opacity=1).next_to(arrRect, DOWN)
        pivotLabel = Text('基准值', font_size=15).next_to(pivotRect, RIGHT)
        pivotLegend = VGroup(pivotRect, pivotLabel)

        finishedRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5,
                                     fill_color=GREY, fill_opacity=1).next_to(pivotRect, DOWN)
        finishedLabel = Text('已确定位置', font_size=15).next_to(finishedRect, RIGHT)
        finishedLegend = VGroup(finishedRect, finishedLabel)

        repeatRect1 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                        fill_color=GREEN, fill_opacity=1)
        repeatRect2 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                        fill_color=PINK, fill_opacity=1).next_to(repeatRect1, RIGHT, 0)
        repeatRect = VGroup(repeatRect1, repeatRect2).next_to(finishedRect, DOWN)
        repeatLabel = Text('相同值', font_size=15).next_to(repeatRect, RIGHT)
        repeatLegend = VGroup(repeatRect, repeatLabel)

        self.legendGroup.add(arrLegend, pivotLegend, finishedLegend, repeatLegend)

        self.play(Create(arrLegend), Create(pivotLegend),
                  Create(finishedLegend), Create(repeatLegend))

    def split(self, start, end):
        brace = self.getBrace(start, end)
        self.play(ReplacementTransform(self.brace, brace))
        self.brace = brace
        pivot = self.arr[end]
        self.markPivot(end)
        p1 = start
        p2 = end - 1
        self.movePointer1(p1, True)
        self.movePointer2(p2, True)
        self.wait(0.5)
        while True:
            while self.arr[p1] < pivot:
                p1 += 1
                self.movePointer1(p1)
            while p1 < p2 and self.arr[p2] > pivot:
                p2 -= 1
                self.movePointer2(p2)
            if p1 >= p2:
                break
            self.swap(p1, p2)
        self.swap(p1, end)
        self.markFinished(p1)

    def quickSort(self, start, end, root, order):
        logger.info("arr:%s start:%d end:%d" % (str(self.arr), start, end))
        if start > end:
            return
        if start == end:
            self.play(root.animate.set_color(GREEN))
            self.markFinished(start)
        else:
            brace = self.getBrace(start, end)
            self.play(ReplacementTransform(self.brace, brace))
            self.play(root.animate.set_color(GREEN))
            self.brace = brace
            pivot = self.arr[end]
            self.markPivot(end)
            p1 = start
            p2 = end - 1
            self.movePointer1(p1, True)
            self.movePointer2(p2, True)
            self.wait(0.5)
            while True:
                while self.arr[p1] < pivot:
                    p1 += 1
                    self.movePointer1(p1)
                while p1 < p2 and self.arr[p2] > pivot:
                    p2 -= 1
                    self.movePointer2(p2)
                if p1 >= p2:
                    break
                self.swap(p1, p2)
            self.swap(p1, end)
            self.markFinished(p1)
            if p1 - 1 >= start and end >= p1 + 1:
                tree1 = MathTex('[%s\\quad%s]' % (start, p1 - 1), stroke_width=2).scale(0.5)
                tree1.next_to(root, DOWN).shift([-config.frame_width / 2 ** (order + 1), 0, 0])
                tree2 = MathTex('[%s\\quad%s]' % (p1 + 1, end), stroke_width=2).scale(0.5)
                tree2.next_to(root, DOWN).shift([config.frame_width / 2 ** (order + 1), 0, 0])
                brace = BraceBetweenPoints(tree1.get_critical_point(DOWN),
                                           tree2.get_critical_point(DOWN), UP, stroke_width=1)
                self.play(Write(brace))
                self.play(Write(tree1), Write(tree2))
            elif p1 - 1 < start and end >= p1 + 1:
                tree1 = None
                tree2 = MathTex('[%s\\quad%s]' % (p1 + 1, end), stroke_width=2).scale(0.5)
                tree2.next_to(root, DOWN)
                arrow = Arrow(start=root.get_critical_point(DOWN), end=tree2.get_critical_point(UP))
                self.play(Write(arrow))
                self.play(Write(tree2))
            elif p1 - 1 >= start and end < p1 + 1:
                tree2 = None
                tree1 = MathTex('[%s\\quad%s]' % (start, p1 - 1), stroke_width=2).scale(0.5)
                tree1.next_to(root, DOWN)
                arrow = Arrow(start=root.get_critical_point(DOWN), end=tree1.get_critical_point(UP))
                self.play(Write(arrow))
                self.play(Write(tree1))
            else:
                tree1 = None
                tree2 = None
            self.quickSort(start, p1 - 1, tree1, order + 1)
            self.quickSort(p1 + 1, end, tree2, order + 1)

    def getBrace(self, i, j):
        return BraceBetweenPoints(self.cards[i].get_critical_point(DOWN + LEFT) + [0, CARD_MAX_HEIGHT, 0],
                                  self.cards[j].get_critical_point(DOWN + RIGHT) + [0, CARD_MAX_HEIGHT, 0],
                                  UP)

    def markPivot(self, index):
        self.play(self.cards[index][0].animate.set_fill(RED))

    def markFinished(self, index):
        self.play(self.cards[index][0].animate.set_fill(GREY))

    def swap(self, i, j):
        if i == j:
            return
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
        path1 = Arc(abs(j - i) * CARD_SPACE / 2, PI, -PI)
        path1.move_to((self.cards[i].get_critical_point(DOWN) + self.cards[j].get_critical_point(DOWN)) / 2,
                      aligned_edge=DOWN)
        path2 = Arc(abs(j - i) * CARD_SPACE / 2, 0, PI)
        path2.move_to((self.cards[i].get_critical_point(DOWN) + self.cards[j].get_critical_point(DOWN)) / 2,
                      aligned_edge=DOWN)
        a, b = min(i, j), max(i, j)
        self.play(MyMoveAlongPath(self.cards[a], path1, aligned_edge=DOWN),
                  MyMoveAlongPath(self.cards[b], path2, aligned_edge=DOWN))
        self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def movePointer1(self, index: int, direct=False):
        if direct:
            self.pointer1.move_to(self.cards[index].get_critical_point(DOWN) + [0, -0.1, 0],
                                  aligned_edge=RIGHT + UP)
        else:
            self.play(self.pointer1.animate
                      .move_to(self.cards[index].get_critical_point(DOWN) + [0, -0.1, 0],
                               aligned_edge=RIGHT + UP))

    def movePointer2(self, index: int, direct=False):
        if direct:
            self.pointer2.move_to(self.cards[index].get_critical_point(DOWN) + [0, -0.1, 0],
                                  aligned_edge=LEFT + UP)
        else:
            self.play(self.pointer2.animate.move_to(self.cards[index].get_critical_point(DOWN) + [0, -0.1, 0],
                                                    aligned_edge=LEFT + UP))

    def setArray(self, arr, repeat_val, base_y=0.5):
        initPos = -(CARD_SPACE * len(arr) - CARD_SPACE + CARD_WIDTH) / 2
        color_index = 0
        for i, v in enumerate(arr):
            if v == repeat_val:
                if color_index == 0:
                    fillColor = PINK
                    color_index = 1
                else:
                    fillColor = GREEN
            else:
                fillColor = BLUE
            card = VGroup()
            rect = RoundedRectangle(0.1, width=CARD_WIDTH,
                                    height=CARD_MIN_HEIGHT + (v - 10) / 90 * (CARD_MAX_HEIGHT - CARD_MIN_HEIGHT),
                                    fill_color=fillColor, fill_opacity=1) \
                .move_to([initPos + i * CARD_SPACE, base_y, 0], aligned_edge=DOWN + LEFT)
            num = DecimalNumber(v, num_decimal_places=0).move_to(rect.get_center())
            card.add(rect, num)
            self.cards.append(card)
            self.cardGroup.add(card)
        return self.cardGroup

    def getPointer(self, index, scale=0.2):
        if index == 0:
            pointer = VGroup()
            polygon = Polygon([0, 0, 0], [0, -2, 0], [1, -2, 0], [1, -1, 0],
                              fill_opacity=1, fill_color=WHITE, stroke_color=WHITE) \
                .flip() \
                .scale(scale) \
                .move_to(self.cards[0].get_critical_point(DOWN) + [0, -0.1, 0], aligned_edge=RIGHT + UP)
            text = Text("L", font_size=20, fill_color=BLACK, fill_opacity=1) \
                .move_to(polygon.get_critical_point(DOWN), aligned_edge=DOWN)
            pointer.add(polygon, text)
            return pointer
        else:
            pointer = VGroup()
            polygon = Polygon([0, 0, 0], [0, -2, 0], [1, -2, 0], [1, -1, 0],
                              fill_opacity=1, fill_color=WHITE, stroke_color=WHITE) \
                .scale(scale) \
                .move_to(self.cards[-2].get_critical_point(DOWN) + [0, -0.1, 0], aligned_edge=LEFT + UP)
            text = Text("R", font_size=20, fill_color=BLACK, fill_opacity=1) \
                .move_to(polygon.get_critical_point(DOWN), aligned_edge=DOWN)
            pointer.add(polygon, text)
            return pointer
