import numpy as np

from manim import *
from my_ctex import my_ctex

CARD_WIDTH = 0.4
CARD_SPACE = 0.6
CARD_MAX_HEIGHT = 1
CARD_MIN_HEIGHT = 0.4
RUN_TIME = 0.5


class ShellSortScene(Scene):
    def construct(self):
        self.title = Tex('选择排序',
                         tex_template=my_ctex(), font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.add(self.title)
        self.note1 = Tex(r'由于插入排序只能交换相邻的元素，因此对于大规模的乱序数组插入排序非常慢，大的元素必须从左侧一格一格到最右侧。希尔排序是对插入排序'
                         r'的改进，其思想是使数组中任意间隔h的元素是有序的，这样，h很大的时候，元素每次移动都能到很远的地方，h从大的值不断减小到1，这样，h很大时，'
                         r'需要排序的数组长度短，h变小后，数组已经是部分有序的了，这样就可以极大地减少移动的次数了，从而改善插入排序的性能。\\'
                         r'希尔排序中h的序列可以有多种选择，一般来说各种递增序列构造的h序列，其希尔排序的性能差异并不十分显著，右侧代码中使用的是的$h(n+1)=3\times h(n)+1$'
                         r'序列。',
                         tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, SMALL_BUFF)
        self.play(Create(self.note1))
        self.code = Code('shell_sort.py', language='python', font_size=20, line_spacing=0.8) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(RIGHT, SMALL_BUFF)
        self.play(Create(self.code))
        self.wait(2)
        self.play(Uncreate(self.note1), Uncreate(self.code))
        self.note2 = Tex('下面是对希尔排序的演示。为了表示希尔排序的思想，演示并没有采用代码清单里面的元素移动方法(即每个元素移动时移动h格，各个子数组交叉运行)，'
                         '而是对每个子数组进行插入排序，因为数组长度较小，这里h的序列采用的是$[7\quad4\quad1]$。',
                         tex_template=my_ctex(40), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, SMALL_BUFF)
        self.play(Create(self.note2))
        self.array = [54, 67, 22, 92, 79, 73, 30, 60, 30, 16, 41, 99, 86, 10, 48]
        # self.array = np.linspace(10, 99, 15, dtype=np.int)
        # self.array[3] = 30
        # self.array[4] = 30
        # np.random.shuffle(self.array)
        self.arrays = [np.copy(self.array)]
        self.repeat_val = 30
        self.cards = []
        self.pointer = None
        self.step = None
        self.cardGroup = self.generateCards(0)
        self.play(Create(self.cardGroup))
        self.wait(1)
        self.sort()
        self.wait(1)
        self.play(Uncreate(self.note2), Uncreate(self.cardGroup), Uncreate(self.pointer), Uncreate(self.step))
        self.array = self.arrays[0]
        #
        # note4 = Tex(r'希尔排序是一种不稳定的排序方法，两个33的位置前后发生了变化，这是因为当h较大时，元素移动会跨越较多的格子从而跑到相邻元素的前面，'
        #             r'插入排序的最差时间复杂度为$O(n^{1.5})$。插入排序的代码量很小，且不需要额外的内存空间，因此在需要直接操作硬件或者在嵌入式系统中时'
        #             r'可以先使用希尔排序进行排序，如果不满足速度要求再更换其他的更快的排序算法.',
        #             tex_template=my_ctex(22), tex_environment='flushleft', font_size=28).next_to(self.title, DOWN,
        #                                                                                          MED_LARGE_BUFF) \
        #     .to_edge(LEFT, SMALL_BUFF)
        # self.code = Code('shell_sort.py', language='python', font_size=20, line_spacing=0.8) \
        #     .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(RIGHT, SMALL_BUFF)
        # self.play(Create(note4), Create(self.code))
        #
        # self.wait(2)

    def sort(self):
        pass

    def swap(self, i, j):
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self.play(self.cards[j].animate(run_time=RUN_TIME).shift([CARD_SPACE * abs(j - i), 0, 0]),
                  self.cards[i].animate(run_time=RUN_TIME).shift([-CARD_SPACE * abs(j - i), 0, 0]))
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