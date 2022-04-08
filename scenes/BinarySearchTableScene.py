from manim import *
from scenes.BinarySearchTable import BinarySearchTable
from scenes.my_ctex import my_ctex
from widgets.scene import MScene
from widgets.ZCurveArrow import ZCurveArrow
from widgets.Struct import Struct

CARD_WIDTH = 0.5
CARD_SPACE = 1
CARD_MAX_HEIGHT = 1.5
CARD_MIN_HEIGHT = 0.5
RUN_TIME = 0.5


class BinarySearchTableScene(MScene):
    def construct(self):
        self.drawGrid()
        svg = SVGMobject('assets/dog3.svg', color=BLACK, fill_opacity=1, stroke_opacity=0, height=1).to_edge(LEFT + UP,
                                                                                                             buff=SMALL_BUFF)
        self.add(svg)
        self.title = Tex('二分查找表',
                         tex_template=my_ctex(), font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.play(Create(self.title))
        self.note1 = Tex(r'利用链表实现的无序查找表在查找时只能通过遍历表直到找到对应键值或者到达末尾添加新节点，这使得查找操作效率很低。有序查找表'
                         r'通过使表中键值对存储时根据键的值排序，从而维护一张键有序表，通过利用键的顺序信息，可以加速表的查找速度。\\'
                         r'二分法有序数组查找是一种古老而有效的查找算法，他通过每次将有序数组分割为两半，然后在目标值所在的一半继续划分，从而使得查找'
                         r'操作的时间复杂度降低为$O(\text{log}N)$，如下图所示：',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))

        self.cards = []
        self.cardGroup = VGroup()
        self.pointer = None
        self.lpointer = None
        self.rpointer = None

        self.arr = [11, 22, 33, 44, 55, 66, 77, 88, 99]
        self.setArray(self.arr, base_y=-2.5)
        self.play(Create(self.cardGroup, run_time=RUN_TIME))

        self.wait(1)

        self.note2 = Tex(r'现在我们要从数组中寻找11这个数,',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note1, DOWN, SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note2))

        self.wait(1)

        temp = self.rank(11)

        self.wait(1)

        self.note3 = Tex(r'然后我们要寻找99这个数.',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note2, RIGHT, SMALL_BUFF)
        self.play(Create(self.note3))
        self.cards[temp].set_stroke(WHITE)

        self.wait(1)

        temp = self.rank(99)

        self.wait(1)

        self.note4 = Tex(r'显然,对于任意位置的数，查找操作的数组访问次数不会超过$\text{log}(N)+1$次，作出如下假设，当要查找'
                         r'的数不存在时，应返回不小于该数的最小索引，比如我们要查找50这个数',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note1, DOWN, SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Uncreate(self.note2), Uncreate(self.note3))
        self.play(Create(self.note4))
        self.cards[temp].set_stroke(WHITE)

        self.wait(1)

        temp = self.rank(50)

        self.wait(1)

        self.play(Uncreate(self.note1), Uncreate(self.note2), Uncreate(self.note3), Uncreate(self.note4), Uncreate(self.pointer),
                  Uncreate(self.cardGroup))

        self.note1 = Tex(r'下面是二分查找的c代码：',
                         tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))

        self.code1 = Code('binary_search_table_struct.c', language='c', font_size=20, line_spacing=0.5, insert_line_no=False,
                          margin=0.1) \
            .next_to(self.note1, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)

        self.code2 = Code('rank.c', language='c', font_size=20, line_spacing=0.5, insert_line_no=False,
                          margin=0.1) \
            .next_to(self.title, DOWN, MED_SMALL_BUFF).to_edge(RIGHT, LARGE_BUFF)
        self.play(Create(self.code1), Create(self.code2))

        self.wait(3)

        self.play(Uncreate(self.code1), Uncreate(self.code2), Uncreate(self.note1))

        self.note1 = Tex(r'下面我们来看基于二分法的有序查找表的实现，显然，在引入rank函数后，查找操作变得十分简单，我们下面来分析值的更新以及键值'
                         r'的插入和删除,我们以一个字母ASCII表为例。',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))

        self.wait(0.5)

        bst = BinarySearchTable(self, 10, posX=-config.frame_x_radius + 1, posY=-3)
        bst.initScene()

        self.note2 = Tex(r'首先我们往表中加入一些键值对，A:50, C:50, E:52',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note1, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note2))
        #
        bst.put('A', 50)
        bst.put('C', 50)
        bst.put('E', 52)

        self.note3 = Tex(r'继续插入B:49, D:51, F:53',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note2, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note3))
        bst.put('B', 49)
        bst.put('D', 51)
        bst.put('F', 53)

        self.wait(1)

        self.note4 = Tex(r'这时我们发现A的ASCII码输错了，因此我们要将其更新为正确的值48：',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note3, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note4))
        bst.put('A', 48)

        self.wait(1)

        self.note5 = Tex(r'接下来我们从表中删除A',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note4, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note5))
        bst.delete('A')

        self.wait(1)

        self.play(Uncreate(self.note2), Uncreate(self.note3), Uncreate(self.note4), Uncreate(self.note5))

        self.note2 = Tex(r'显然，可以看出，对于更新键值，二分查找表的速度很快，时间复杂度为$O(\text{log}N)$，但是对于插入新键值或者是删除键值，'
                         r'则需要根据插入或删除的位置移动数组，尤其是插入或删除的位置在首元素时，需要移动整个数组，此时，平均时间复杂度为$O(\text{N})$.\\'
                         r'二分查找表实现简单，用途广泛，适用于初始化时键已经处于排序状态且运行过程中很少插入或删除值的场合，但对于大数据量且需要频繁插入删除'
                         r'的场合，二分查找效率并不高。',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note1, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note2))


        self.wait(3)

        self.play(Uncreate(self.note1), Uncreate(self.note2), *bst.clearScene())

        self.code1 = Code('binary_search_table_delete.c', language='c', font_size=15, line_spacing=0.5, insert_line_no=False,
                          margin=0.1) \
            .next_to(self.title, DOWN, MED_SMALL_BUFF).to_edge(RIGHT, MED_SMALL_BUFF)

        self.code2 = Code('binary_search_table_put.c', language='c', font_size=16, line_spacing=0.5,
                          insert_line_no=False,
                          margin=0.1) \
            .next_to(self.title, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.code1), Create(self.code2))

        self.wait(3)

        self.play(Uncreate(self.title), Uncreate(self.code1), Uncreate(self.code2))

        self.title = Tex('参考资料',
                         tex_template=my_ctex(), font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.play(Create(self.title))
        self.note1 = Tex(r'[1]算法:第4版/(美)塞奇威克,(美)韦恩 著;谢路云 译.-- 北京:人民邮电出版社,2012.10',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))

    def setArray(self, arr, base_y=0.5):
        initPos = -(CARD_SPACE * len(arr) - CARD_SPACE + CARD_WIDTH) / 2
        color_index = 0
        for i, v in enumerate(arr):
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

    def rank(self, key):
        if len(self.arr) == 0:
            return 0
        low = 0
        high = len(self.arr) - 1
        posX = self.cardGroup.get_left()[0]
        posY = self.cardGroup.get_critical_point(UP)[1]
        self.wait(0.5)
        self.lpointer = self.generateLRPointer(LEFT, 'L').move_to(
            [posX + low * CARD_SPACE + CARD_WIDTH / 2, self.cards[0].get_critical_point(DOWN)[1] - SMALL_BUFF, 0],
            UP + RIGHT)
        self.rpointer = self.generateLRPointer(RIGHT, 'H').move_to(
            [posX + high * CARD_SPACE + CARD_WIDTH / 2, self.cards[0].get_critical_point(DOWN)[1] - SMALL_BUFF, 0],
            UP + LEFT)
        self.play(FadeIn(self.lpointer, run_time=RUN_TIME), FadeIn(self.rpointer, run_time=RUN_TIME))
        while low <= high:
            mid = (low + high) // 2
            if self.pointer == None:
                self.pointer = self.generatePointer().move_to(
                    self.cards[mid].get_critical_point(UP) + [0, SMALL_BUFF, 0], DOWN)
                self.play(Create(self.pointer, run_time=RUN_TIME))
            else:
                self.play(self.pointer.animate(run_time=RUN_TIME).move_to(
                    self.cards[mid].get_critical_point(UP) + [0, SMALL_BUFF, 0], DOWN))
            if self.arr[mid] == key:
                self.cards[mid][0].set_stroke(RED)
                self.play(FadeOut(self.lpointer, run_time=RUN_TIME),
                          FadeOut(self.rpointer, run_time=RUN_TIME))
                self.lpointer = None
                self.rpointer = None
                return mid
            if self.arr[mid] > key:
                high = mid - 1
            else:
                low = mid + 1
            if low > high:
                self.lpointer[0].set_color(RED)
                self.rpointer[0].set_color(RED)
            self.play(
                self.lpointer.animate(run_time=RUN_TIME).move_to(
                    [posX + low * CARD_SPACE + CARD_WIDTH / 2, self.cards[0].get_critical_point(DOWN)[1] - SMALL_BUFF,
                     0],
                    UP + RIGHT),
                self.rpointer.animate(run_time=RUN_TIME).move_to(
                    [posX + high * CARD_SPACE + CARD_WIDTH / 2, self.cards[0].get_critical_point(DOWN)[1] - SMALL_BUFF,
                     0],
                    UP + LEFT))
        self.cards[low][0].set_stroke(RED)
        self.play(FadeOut(self.lpointer, run_time=RUN_TIME),
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
                              fill_opacity=0, fill_color=WHITE, stroke_color=WHITE, stroke_width=3) \
                .flip() \
                .scale(scale)
            text = Text(text, font_size=18, fill_color=WHITE, fill_opacity=1) \
                .move_to(polygon.get_critical_point(DOWN), aligned_edge=DOWN)
            pointer.add(polygon, text)
            return pointer
        else:
            pointer = VGroup()
            polygon = Polygon([0, 0, 0], [0, -2, 0], [1, -2, 0], [1, -1, 0],
                              fill_opacity=0, fill_color=WHITE, stroke_color=WHITE, stroke_width=3) \
                .scale(scale)
            text = Text(text, font_size=18, fill_color=WHITE, fill_opacity=1) \
                .move_to(polygon.get_critical_point(DOWN), aligned_edge=DOWN)
            pointer.add(polygon, text)
            return pointer
