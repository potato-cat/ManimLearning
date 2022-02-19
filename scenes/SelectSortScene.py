import numpy as np

from manim import *
from my_ctex import my_ctex
from scenes.my_movement import MyMoveAlongPath

CARD_WIDTH = 0.5
CARD_SPACE = 0.8
CARD_MAX_HEIGHT = 1
CARD_MIN_HEIGHT = 0.5
RUN_TIME = 0.5


class SelectSortScene(Scene):
    def construct(self):
        self.title = Tex('选择排序',
                         tex_template=my_ctex(), font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.add(self.title)
        self.note1 = Tex(r'选择排序的思想是每次循环找出当前段的最小值然后与左侧值交换位置，首先，找到数组中最小的元素，'
                         r'然后将它和数组中第一个元素交换位置，再次，在剩下的元素里面找到最小的元素，将它与数组的第二个元素'
                         r'交换位置。如此往复，直到整个数组排序。其算法如有图所示。',
                         tex_template=my_ctex(24), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))
        self.code = Code('select_sort.py', language='python', font_size=20, line_spacing=0.5) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(RIGHT, MED_SMALL_BUFF)
        self.play(Create(self.code))
        self.wait(1)
        self.note2 = Tex(r'下面是选择排序的动画演示：',
                         tex_template=my_ctex(24), tex_environment='flushleft', font_size=28) \
            .next_to(self.note1, DOWN, SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note2))
        # , 41, 99, 86, 10, 48
        self.array = [30, 54, 67, 22, 92, 79, 73, 60, 30, 16]

        self.repeat_val = 30
        self.cards = []
        self.pointer = None
        self.minText = Tex(r'最小值:',
                           tex_template=my_ctex(22), tex_environment='flushleft', font_size=28)
        self.minRect = Rectangle(height=0.4, width=0.8, stroke_width=2)
        self.minVal = DecimalNumber(0, 0, font_size=28)
        self.indexText = Tex(r'最小值索引:',
                             tex_template=my_ctex(22), tex_environment='flushleft', font_size=28)
        self.indexRect = Rectangle(height=0.4, width=0.8, stroke_width=2)
        self.indexVal = DecimalNumber(0, 0, font_size=28)

        self.cardGroup = self.generateCards(-3)
        self.iVal = Tex(r'$i=0$',
                        tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
            .next_to(self.cardGroup, UP).to_edge(LEFT)
        self.jVal = Tex(r'$j=0$',
                        tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
            .next_to(self.iVal, RIGHT)
        self.legend = self.generateLegend().next_to(self.code, DOWN, MED_SMALL_BUFF).to_edge(RIGHT)
        self.play(Create(self.cardGroup), Create(self.legend), Create(self.iVal), Create(self.jVal))
        self.wait(1)
        self.sort()
        self.wait(1)
        self.play(Uncreate(self.note2), Uncreate(self.note1))
        #
        self.note3 = Tex(r'选择排序时间复杂度为$O(N^2)$，需要$~N^2/2$次比较以及$N$次交换，选择排序的运行时间与输入无关，它不会因为数组'
                         r'的排序状态而改变比较次数以及移动次数，并且它的数据移动次数是所有排序方式中最少的。另外，选择排序是一种不稳定的排序算法，'
                         r'排序前后两个30的位置放生了交换，这是因为在发生最小值交换时，会将相同的数从左侧交换到右侧。',
                         tex_template=my_ctex(24), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note3))
        self.wait(3)

    def generateLegend(self, buff=1):
        legendGroup = VGroup()
        arrRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5,
                                   fill_color=BLUE, fill_opacity=1)
        arrLabel = Text('未排序数组', font_size=15).next_to(arrRect, RIGHT)
        arrLegend = VGroup(arrRect, arrLabel).to_edge(RIGHT, buff=0).to_edge(UP, buff=buff)

        pivotRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5,
                                     fill_color=RED, fill_opacity=1).next_to(arrRect, DOWN)
        pivotLabel = Text('当前最小值', font_size=15).next_to(pivotRect, RIGHT)
        pivotLegend = VGroup(pivotRect, pivotLabel)

        repeatRect1 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                       fill_color=GREEN, fill_opacity=1)
        repeatRect2 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                       fill_color=PINK, fill_opacity=1).next_to(repeatRect1, RIGHT, 0)
        repeatRect = VGroup(repeatRect1, repeatRect2).next_to(pivotRect, DOWN)
        repeatLabel = Text('相同值', font_size=15).next_to(repeatRect, RIGHT)
        repeatLegend = VGroup(repeatRect, repeatLabel)

        legendGroup.add(arrLegend, pivotLegend, repeatLegend)

        return legendGroup

    def sort(self):
        p = self.cardGroup.get_critical_point(LEFT + UP)
        self.minText.next_to(p, UP, LARGE_BUFF, aligned_edge=LEFT)
        self.minRect.next_to(self.minText, RIGHT, MED_SMALL_BUFF)
        self.minVal.move_to(self.minRect)
        self.indexText.next_to(self.minRect, RIGHT, MED_SMALL_BUFF)
        self.indexRect.next_to(self.indexText, RIGHT, MED_SMALL_BUFF)
        self.indexVal.move_to(self.indexRect)
        self.play(Create(self.minText), Create(self.minRect), Create(self.indexText), Create(self.indexRect),
                  Create(self.minVal), Create(self.indexVal))
        for i in range(0, len(self.array)):
            min_i = i
            tempColor = self.cards[min_i][0].get_color()
            minVal = DecimalNumber(self.array[min_i], 0, font_size=28).move_to(self.minRect)
            indexVal = DecimalNumber(min_i, 0, font_size=28).move_to(self.indexRect)
            iVal = Tex(r'$i=%d$' % i,
                       tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
                .move_to(self.iVal, LEFT)
            self.play(ReplacementTransform(self.minVal, minVal, run_time=RUN_TIME),
                      ReplacementTransform(self.indexVal, indexVal, run_time=RUN_TIME),
                      self.cards[min_i][0].animate(run_time=RUN_TIME).set_color(RED),
                      ReplacementTransform(self.iVal, iVal, run_time=RUN_TIME))
            self.minVal = minVal
            self.indexVal = indexVal
            self.iVal = iVal
            for j in range(i + 1, len(self.array)):
                p = self.cards[j].get_critical_point(DOWN) - [0, 0.1, 0]
                jVal = Tex(r'$j=%d$' % j,
                           tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
                    .move_to(self.jVal, LEFT)
                if self.pointer == None:
                    self.pointer = self.generatePointer().move_to(p, UP)
                    self.add(self.pointer)
                    self.play(ReplacementTransform(self.jVal, jVal, run_time=0))
                    self.wait(0.5)
                elif j == i + 1:
                    self.pointer.move_to(p, UP)
                    self.play(ReplacementTransform(self.jVal, jVal, run_time=0))
                    self.wait(0.5)
                else:
                    self.play(self.pointer.animate(run_time=RUN_TIME).move_to(p, UP),
                              ReplacementTransform(self.jVal, jVal, run_time=RUN_TIME))
                self.jVal = jVal
                if self.array[j] < self.array[min_i]:
                    minVal = DecimalNumber(self.array[j], 0, font_size=28).move_to(self.minRect)
                    indexVal = DecimalNumber(j, 0, font_size=28).move_to(self.indexRect)
                    temp = self.cards[j][0].get_color()
                    self.play(self.cards[j][0].animate.set_color(RED),
                              self.cards[min_i][0].animate.set_color(tempColor),
                              ReplacementTransform(self.minVal, minVal),
                              ReplacementTransform(self.indexVal, indexVal))
                    self.minVal = minVal
                    self.indexVal = indexVal
                    min_i = j
                    tempColor = temp
            self.swap(i, min_i)

            self.cards[i][0].set_color(tempColor)

    def swap(self, i, j):
        if i == j:
            return
        self.array[i], self.array[j] = self.array[j], self.array[i]
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

    def generateCard(self, v, color=BLUE):
        card = VGroup()
        rect = RoundedRectangle(0.1, width=CARD_WIDTH,
                                height=CARD_MIN_HEIGHT + (v - 10) / 90 * (CARD_MAX_HEIGHT - CARD_MIN_HEIGHT),
                                color=color)
        num = DecimalNumber(v, num_decimal_places=0, font_size=30).move_to(rect.get_center())
        card.add(rect, num)
        return card

    def generatePointer(self):
        return Triangle(color=WHITE, stroke_width=2).scale(0.1)

    def generateCards(self, base_y):
        arr = self.array
        base_x = -(CARD_SPACE * len(self.array) - CARD_SPACE + CARD_WIDTH) / 2
        color_index = 0
        cardGroup = VGroup()
        for i, v in enumerate(arr):
            if v == self.repeat_val:
                if color_index == 0:
                    color = PINK
                    color_index = 1
                else:
                    color = GREEN
            else:
                color = BLUE
            card = self.generateCard(v, color=color) \
                .move_to([base_x + i * CARD_SPACE, base_y, 0], aligned_edge=DOWN + LEFT)
            self.cards.append(card)
            cardGroup.add(card)
        return cardGroup

# 传送阵:
# 1. https://www.bilibili.com/video/BV1434y1C7z9
# 2. https://www.bilibili.com/video/BV1CL4y1s7DQ
# 3. https://www.bilibili.com/video/BV1x44y1W7mQ
# 4. https://www.bilibili.com/video/BV1Za411m7LT
# 5. https://www.bilibili.com/video/BV1RR4y1K7R9
# 6. https://www.bilibili.com/video/BV1Gu411X7TH
