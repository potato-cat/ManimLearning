import numpy as np

from manim import *
from my_ctex import my_ctex
from scenes.my_movement import MyMoveAlongPath

CARD_WIDTH = 0.5
CARD_SPACE = 0.8
CARD_MAX_HEIGHT = 1
CARD_MIN_HEIGHT = 0.5
RUN_TIME = 0.5


class BubbleSortScene(Scene):
    def construct(self):
        self.title = Tex('冒泡排序',
                         tex_template=my_ctex(), font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.add(self.title)
        self.note1 = Tex(r'冒泡排序的思想是每次比较相邻的两个值，若左侧值较大则交换两个值顺序，如此循环一轮则，最大值将“冒泡”到'
                         r'最右侧，然后下一轮循环中，将剩余的值中的最大值“冒泡”到最右侧，如此循环n-1轮，排序完成。\\'
                         r'其算法如有图所示。',
                         tex_template=my_ctex(24), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))
        self.code = Code('bubble_sort.py', language='python', font_size=20, line_spacing=0.5) \
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
        self.rect = None

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
        self.note3 = Tex(r'冒泡排序时间复杂度为$O(N^2)$，需要$N(N-1)/2$次比较以及最多$N(N-1)/2$次交换，冒泡排序是一种稳定的排序算法，'
                         r'排序前后两个30的位置未发生交换。',
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

        repeatRect1 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                       fill_color=GREEN, fill_opacity=1)
        repeatRect2 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                       fill_color=PINK, fill_opacity=1).next_to(repeatRect1, RIGHT, 0)
        repeatRect = VGroup(repeatRect1, repeatRect2).next_to(arrRect, DOWN)
        repeatLabel = Text('相同值', font_size=15).next_to(repeatRect, RIGHT)
        repeatLegend = VGroup(repeatRect, repeatLabel)

        legendGroup.add(arrLegend, repeatLegend)

        return legendGroup

    def createRect(self, i, j):
        left_down = self.cards[0].get_critical_point(LEFT+DOWN) - np.array([(CARD_SPACE-CARD_WIDTH)/2, 0.1, 0])
        rect = Rectangle(width=abs(i-j)*CARD_SPACE, height=CARD_MAX_HEIGHT+0.2)
        rect.move_to(left_down, LEFT+DOWN)
        return rect


    def sort(self):
        p = self.cardGroup.get_critical_point(LEFT + UP)
        for i in range(0, len(self.array) - 1):
            iVal = Tex(r'$i=%d$' % i,
                       tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
                .move_to(self.iVal, LEFT)
            self.play(ReplacementTransform(self.iVal, iVal, run_time=RUN_TIME))
            self.iVal = iVal
            rect = self.createRect(0, len(self.array) - i)
            if self.rect == None:
                self.rect = rect
                self.play(Create(self.rect, run_time=RUN_TIME))
            else:
                self.play(ReplacementTransform(self.rect, rect, run_time=RUN_TIME))
                self.rect = rect
            for j in range(0, len(self.array) - 1 - i):
                p = self.cards[j].get_critical_point(DOWN) - [0, 0.1, 0]
                jVal = Tex(r'$j=%d$' % j,
                           tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
                    .move_to(self.jVal, LEFT)
                if self.pointer == None:
                    self.pointer = self.generatePointer().move_to(p, UP)
                    self.add(self.pointer)
                    self.play(ReplacementTransform(self.jVal, jVal, run_time=0))
                    self.wait(0.5)
                elif j == 0:
                    self.pointer.move_to(p, UP)
                    self.play(ReplacementTransform(self.jVal, jVal, run_time=0))
                    self.wait(0.5)
                else:
                    self.play(self.pointer.animate(run_time=RUN_TIME).move_to(p, UP),
                              ReplacementTransform(self.jVal, jVal, run_time=RUN_TIME))
                self.jVal = jVal
                if self.array[j] > self.array[j+1]:
                    self.swap(j, j+1)


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
        self.play(MyMoveAlongPath(self.cards[a], path1, aligned_edge=DOWN, run_time=RUN_TIME),
                  MyMoveAlongPath(self.cards[b], path2, aligned_edge=DOWN, run_time=RUN_TIME))
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
