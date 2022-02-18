from manim import *
from my_ctex import my_ctex

CARD_WIDTH = 0.5
CARD_SPACE = 1
CARD_MAX_HEIGHT = 1
CARD_MIN_HEIGHT = 0.5


class InsertSortScene(Scene):
    def construct(self):
        self.title = Tex('插入排序',
                         tex_template=my_ctex, font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.add(self.title)
        note1 = Tex('插入排序通过将元素插入已经有序的数组中从而为元素找到正确的位置,程序实现时，为了给要插入的元素腾个地方出来，'
                    '在插入位置与待插入元素之间的元素均需右移，代码如右侧所示。',
                    tex_template=my_ctex, tex_environment='flushleft', font_size=30).next_to(self.title, DOWN) \
            .to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(note1))
        self.code = Code('insert_sort.py', language='python', font_size=20).next_to(self.title, DOWN) \
            .to_edge(RIGHT, MED_SMALL_BUFF)
        self.play(Create(self.code))
        self.legend = self.createLegend()
        note2 = Tex('下面是对有序数组进行插入操作的演示。',
                    tex_template=my_ctex, tex_environment='flushleft', font_size=30).next_to(note1, DOWN) \
            .to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(note2))
        self.array = [11, 22, 33, 66, 77, 88, 99, 55]
        self.repeat_val = None
        self.cards = []
        self.cardGroup = VGroup()
        self.pointer = None
        self.generateCards(-3)
        self.play(Create(self.cardGroup), Create(self.legend))
        self.wait(1)
        i = 7
        card = self.cards[i]
        self.play(card.animate.shift([0, CARD_MAX_HEIGHT + SMALL_BUFF, 0]))
        for j in range(i, 0, -1):
            p = self.cards[j - 1].get_critical_point(DOWN)
            if self.pointer == None:
                self.pointer = Arrow(start=p - [0, LARGE_BUFF, 0], end=p)
                self.play(Create(self.pointer))
            elif j == i:
                self.pointer.move_to(p, UP)
            else:
                self.play(self.pointer.animate.move_to(p, UP))
            if self.array[j] < self.array[j - 1]:
                self.swap(j, j - 1)
            else:
                break
        self.play(card.animate.shift([0, -CARD_MAX_HEIGHT - SMALL_BUFF, 0]))
        self.wait(1)
        self.play(Uncreate(note2), Uncreate(self.pointer))

        note3 = Tex('下面是对数组排序的演示。',
                    tex_template=my_ctex, tex_environment='flushleft', font_size=30).next_to(note1, DOWN) \
            .to_edge(LEFT, MED_SMALL_BUFF)

        temp = self.cardGroup
        self.array = [33, 22, 77, 55, 99, 33, 66, 11]
        self.repeat_val = 33
        self.cards = []
        self.cardGroup = VGroup()
        self.pointer = None
        self.generateCards(-3)
        self.play(Create(note3), ReplacementTransform(temp, self.cardGroup))
        self.wait(1)
        self.sort()
        self.wait(1)

        self.play(Uncreate(note3), Uncreate(note1))
        note4 = Tex(r'插入排序是一种稳定的排序方法，两个33的位置前后没有发生变化，插入排序的时间复杂度为$O(n^2)$，在最差的情况下，'
                    r'需要$~\frac{n^2}{2}$次比较以及$~\frac{n^2}{2}$次交换(即反向)，最好的情况需要$n-1$次比较和0次交换(即排序完成)',
                    tex_template=my_ctex, tex_environment='flushleft', font_size=30).next_to(self.title, DOWN) \
            .to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(note4))

        self.wait(2)

    def createLegend(self):
        legend = VGroup()
        arrRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5,
                                   fill_color=BLUE, fill_opacity=1)
        arrLabel = Text('未排序数组', font_size=20).next_to(arrRect, RIGHT)
        arrLegend = VGroup(arrRect, arrLabel).next_to(self.code, DOWN).to_edge(RIGHT)

        repeatRect1 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                       fill_color=GREEN, fill_opacity=1)
        repeatRect2 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                       fill_color=PINK, fill_opacity=1).next_to(repeatRect1, RIGHT, 0)
        repeatRect = VGroup(repeatRect1, repeatRect2).next_to(arrRect, DOWN)
        repeatLabel = Text('相同值', font_size=20).next_to(repeatRect, RIGHT)
        repeatLegend = VGroup(repeatRect, repeatLabel)

        arrow = Arrow(start=ORIGIN, end=RIGHT).next_to(repeatRect, DOWN)
        arrowLabel = Text('当前的j', font_size=20).next_to(arrow, RIGHT)
        arrowLegend = VGroup(arrow, arrowLabel)

        legend.add(arrLegend, repeatLegend, arrowLegend)
        return legend

    def sort(self):
        for i in range(1, len(self.array)):
            card = self.cards[i]
            self.play(card.animate.shift([0, CARD_MAX_HEIGHT + SMALL_BUFF, 0]))
            for j in range(i, 0, -1):
                p = self.cards[j - 1].get_critical_point(DOWN)
                if self.pointer == None:
                    self.pointer = Arrow(start=p - [0, LARGE_BUFF, 0], end=p)
                    self.play(Create(self.pointer))
                elif j == i:
                    self.pointer.move_to(p, UP)
                    self.wait(0.5)
                else:
                    self.play(self.pointer.animate.move_to(p, UP))
                if self.array[j] < self.array[j - 1]:
                    self.swap(j, j - 1)
                else:
                    break
            self.play(card.animate.shift([0, -CARD_MAX_HEIGHT - SMALL_BUFF, 0]))

    def swap(self, i, j):
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self.play(self.cards[j].animate.shift([CARD_SPACE, 0, 0]),
                  self.cards[i].animate.shift([-CARD_SPACE, 0, 0]))
        self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def generateCard(self, v, color=BLUE):
        card = VGroup()
        rect = RoundedRectangle(0.1, width=CARD_WIDTH,
                                height=CARD_MIN_HEIGHT + (v - 10) / 90 * (CARD_MAX_HEIGHT - CARD_MIN_HEIGHT),
                                color=color)
        num = DecimalNumber(v, num_decimal_places=0).move_to(rect.get_center())
        card.add(rect, num)
        return card

    def generateCards(self, base_y):
        arr = self.array
        base_x = -(CARD_SPACE * len(self.array) - CARD_SPACE + CARD_WIDTH) / 2
        color_index = 0
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
            self.cardGroup.add(card)
        return self.cardGroup

