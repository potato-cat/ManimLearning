from my_movement import MyMoveAlongPath
from manim import *
import numpy as np
from my_ctex import my_ctex

CARD_WIDTH = 0.5
CARD_SPACE = 0.8
CARD_MAX_HEIGHT = 1
CARD_MIN_HEIGHT = 0.5


class MergeSortScene(Scene):
    def construct(self):
        self.title = Tex('归并排序', tex_environment='center', tex_template=my_ctex).to_edge(UP)
        self.add(self.title)
        self.initScene()
        note1 = Tex(r'归并排序是另一种基于“分而治之”思想的排序方法，归并是将两个有序的数组归并成为一个更大的有序数组。'
                    r'归并排序通过递归地将它分成两半分别排序，然后将结果归并起来。\\'
                    r'下面是一种归并的实现：', tex_environment='flushleft',
                    tex_template=my_ctex, font_size=30).next_to(self.title, DOWN).to_edge(LEFT)
        self.section.add(note1)
        self.play(Create(note1))
        self.array = [22, 33, 77, 33, 55, 66, 99]
        self.repeat_val = 33
        self.temp = np.zeros(len(self.array))
        self.generateCards(-CARD_MAX_HEIGHT - 0.5)
        self.section.add(self.cardGroup, self.cardGroup2)
        self.play(Create(self.cardGroup),
                  Create(self.cardGroup2))
        self.wait(1)
        self.setCodePos = lambda x: x.next_to(self.cardGroup, RIGHT).to_edge(RIGHT, MED_SMALL_BUFF)
        self.merge(0, 2, 6)
        self.section.add(self.codeBlock, self.braceL, self.braceR, self.pointer1, self.pointer2)
        self.wait(1)
        self.play(Uncreate(self.section))

        self.initScene()
        note2 = Tex(r'归并排序时，由递归的特性，数组将会被切分为单个数字后才会开始第一次归并，即按照深度优先的方式运行。\\',
                    tex_environment='flushleft',
                    tex_template=my_ctex, font_size=30).next_to(self.title, DOWN).to_edge(LEFT)
        note3 = Tex(r'下面是归并排序的实现。', tex_environment='flushleft',
                    tex_template=my_ctex, font_size=30).next_to(note2, DOWN, SMALL_BUFF).to_edge(LEFT)
        self.play(Create(note2), Create(note3))
        self.algoCode1 = Code('sort.py', language='python', font_size=20).next_to(note3, DOWN, SMALL_BUFF) \
            .to_edge(LEFT)
        self.algoCode2 = Code('merge.py', language='python', font_size=20).next_to(note3, DOWN, SMALL_BUFF) \
            .to_edge(RIGHT)

        self.play(Create(self.algoCode1), Create(self.algoCode2))
        self.wait(1)
        self.play(Uncreate(self.algoCode1), Uncreate(self.algoCode2), Uncreate(note3))

        note4 = Tex(r'下面是归并排序的动画演示。', tex_environment='flushleft',
                    tex_template=my_ctex, font_size=30).next_to(note2, DOWN).to_edge(LEFT)
        self.play(Create(note4))
        label1 = VGroup()
        text1 = Tex('sort', tex_environment='flushleft',
                    tex_template=my_ctex, font_size=28)
        rect1 = Rectangle(width=text1.width + 0.2, height=text1.height + 0.2,
                          stroke_width=2).move_to(text1)
        label1.add(rect1, text1)
        label1.next_to(note4, RIGHT)
        label2 = VGroup()
        text2 = Tex('merge', tex_environment='flushleft',
                    tex_template=my_ctex, font_size=28)
        rect2 = Rectangle(width=text2.width + 0.2, height=text2.height + 0.2,
                          stroke_width=2, stroke_color=RED).move_to(text2)
        label2.add(rect2, text2)
        label2.next_to(label1, RIGHT)
        self.play(Create(label1))
        self.play(Create(label2))
        self.array = [33, 22, 77, 55, 99, 33, 66]
        self.repeat_val = 33
        self.temp = np.zeros(len(self.array))
        self.generateCards(-CARD_MAX_HEIGHT - 0.5)
        self.cardGroup.to_edge(LEFT)
        self.cardGroup2.to_edge(LEFT)
        self.cardRight = self.cardGroup.get_right()[0]
        self.treeWidth = config.frame_x_radius - self.cardRight
        self.treeCenter = (config.frame_x_radius + self.cardRight) / 2
        self.tree0 = MathTex('a[%d...%d]' % (0, 6), stroke_width=3, font_size=28) \
            .move_to([self.treeCenter, -0.7, 0])
        self.treeTitle = Tex(r'排序依赖树', tex_environment='center',
                             tex_template=my_ctex, font_size=30) \
            .next_to(self.tree0, UP)
        self.play(Create(self.cardGroup),
                  Create(self.cardGroup2),
                  Create(self.tree0),
                  Create(self.treeTitle))
        self.setCodePos = lambda x: x.next_to(self.treeTitle, RIGHT).to_edge(RIGHT, MED_SMALL_BUFF)
        self.sort(0, 6, self.tree0, 1)
        self.wait(1)
        note5 = Tex(r'归并排序是一种稳定的排序算法，它的时间复杂度为$n\text{log}_2n$。',
                    tex_environment='flushleft',
                    tex_template=my_ctex, font_size=30).next_to(note4, DOWN).to_edge(LEFT)
        self.play(Create(note5))
        self.wait(2)

    def initScene(self):
        self.section = VGroup()
        self.cards = []
        self.cards2 = []
        self.codeBlock = None
        self.cardGroup = VGroup()
        self.cardGroup2 = VGroup()
        self.pointer1 = None
        self.pointer2 = None
        self.braceL = None
        self.braceR = None
        self.treeGroup = VGroup()
        self.tree = []

    def sort(self, start, end, tree0, layer):
        if start >= end:
            return
        if self.codeBlock == None:
            self.codeBlock = Code(code='sort(%d, %d)' % (start, end), insert_line_no=False,
                                  background_stroke_width=0,
                                  font_size=20, language='python')
            self.codeBlock = self.setCodePos(self.codeBlock)
            animation = Create(self.codeBlock)
        else:
            codeBlock = self.codeBlock
            self.codeBlock = Code(code='sort(%d, %d)' % (start, end), insert_line_no=False,
                                  background_stroke_width=0,
                                  font_size=20, language='python') \
                .move_to(self.codeBlock, RIGHT)
            animation = ReplacementTransform(codeBlock, self.codeBlock)
        mid = (start + end) // 2
        rect = Rectangle(height=CARD_MAX_HEIGHT + 0.2, width=(end - start + 1) * CARD_SPACE) \
            .move_to((self.cards[start].get_critical_point(DOWN) + self.cards[end].get_critical_point(DOWN)) / 2
                     + np.array([0, -0.1, 0]),
                     aligned_edge=DOWN)
        # codeAnimation = self.addCode('sort(%d, %d)' % (start, end))
        self.play(ShowCreationThenFadeOut(rect), animation)
        if mid > start + 1:
            text1 = 'a[%d...%d]' % (start, mid)
        elif mid > start:
            text1 = 'a[%d,%d]' % (start, mid)
        else:
            text1 = 'a[%d]' % start

        if end > mid + 2:
            text2 = 'a[%d...%d]' % (mid + 1, end)
        elif end > mid + 1:
            text2 = 'a[%d,%d]' % (mid + 1, end)
        else:
            text2 = 'a[%d]' % (mid + 1)

        tree1 = MathTex(text1, stroke_width=2, font_size=28).move_to(
            tree0.get_center() + [-self.treeWidth / 2 ** (layer + 1), -0.6, 0])
        tree2 = MathTex(text2, stroke_width=2, font_size=28).move_to(
            tree0.get_center() + [self.treeWidth / 2 ** (layer + 1), -0.6, 0])
        brace = BraceBetweenPoints(tree1.get_critical_point(UP),
                                   tree2.get_critical_point(UP), UP, buff=0, sharpness=3, stroke_width=0)
        self.play(Create(tree1),
                  Create(tree2),
                  Create(brace))
        self.sort(start, mid, tree1, layer + 1)
        self.sort(mid + 1, end, tree2, layer + 1)
        if self.array[mid] <= self.array[mid + 1]:
            return
        self.merge(start, mid, end)

    def merge(self, start, mid, end):
        if self.codeBlock == None:
            self.codeBlock = Code(code='merge(%d, %d, %d)' % (start, mid, end),
                                  background_stroke_width=0,
                                  insert_line_no=False,
                                  font_size=20, language='python')
            self.codeBlock = self.setCodePos(self.codeBlock)
            animation = Create(self.codeBlock)
        else:
            codeBlock = self.codeBlock
            self.codeBlock = Code(code='merge(%d, %d, %d)' % (start, mid, end),
                                  background_stroke_width=0,
                                  insert_line_no=False,
                                  font_size=20, language='python') \
                .move_to(self.codeBlock, RIGHT)
            animation = ReplacementTransform(codeBlock, self.codeBlock)
        i = start
        j = mid + 1
        rect = Rectangle(height=CARD_MAX_HEIGHT + 0.2, width=(end - start + 1) * CARD_SPACE, color=RED) \
            .move_to((self.cards[start].get_critical_point(DOWN) + self.cards[end].get_critical_point(DOWN)) / 2
                     + np.array([0, -0.1, 0]),
                     aligned_edge=DOWN)
        if self.braceL == None:
            self.braceL = BraceBetweenPoints(
                self.cards[start].get_critical_point(LEFT + DOWN) + [0, CARD_MAX_HEIGHT, 0],
                self.cards[mid].get_critical_point(RIGHT + DOWN) + [0, CARD_MAX_HEIGHT, 0], UP)
            self.braceR = BraceBetweenPoints(
                self.cards[mid + 1].get_critical_point(LEFT + DOWN) + [0, CARD_MAX_HEIGHT, 0],
                self.cards[end].get_critical_point(RIGHT + DOWN) + [0, CARD_MAX_HEIGHT, 0], UP)
            braceAnimations = [Create(self.braceL), Create(self.braceR)]
        else:
            braceL = self.braceL
            braceR = self.braceR
            self.braceL = BraceBetweenPoints(
                self.cards[start].get_critical_point(LEFT + DOWN) + [0, CARD_MAX_HEIGHT, 0],
                self.cards[mid].get_critical_point(RIGHT + DOWN) + [0, CARD_MAX_HEIGHT, 0], UP)
            self.braceR = BraceBetweenPoints(
                self.cards[mid + 1].get_critical_point(LEFT + DOWN) + [0, CARD_MAX_HEIGHT, 0],
                self.cards[end].get_critical_point(RIGHT + DOWN) + [0, CARD_MAX_HEIGHT, 0], UP)
            braceAnimations = [ReplacementTransform(braceL, self.braceL),
                               ReplacementTransform(braceR, self.braceR)]
        self.play(ShowCreationThenFadeOut(rect), animation, *braceAnimations)
        animations = []
        for k in range(start, end + 1):
            self.temp[k] = self.array[k]
            card = self.generateCard(self.array[k], color=self.cards[k][0].get_color()) \
                .move_to(self.cards2[k], DOWN)
            animations.append(ReplacementTransform(self.cards2[k], card))
            arrow = Arrow(start=self.cards[k][0].get_critical_point(DOWN),
                          end=card[0].get_critical_point(UP),
                          buff=SMALL_BUFF, stroke_width=2)
            animations.append(ShowCreationThenFadeOut(arrow))
            self.cardGroup2.remove(self.cards2[k])
            self.cardGroup2.add(card)
            self.cards2[k] = card
        self.play(*animations)
        if self.pointer1 == None:
            self.pointer1 = Arrow(start=ORIGIN, end=[0, 1, 0]) \
                .move_to(self.cards2[i].get_critical_point(DOWN), UP)
            self.pointer2 = Arrow(start=ORIGIN, end=[0, 1, 0]) \
                .move_to(self.cards2[j].get_critical_point(DOWN), UP)
            self.play(Create(self.pointer1),
                      Create(self.pointer2))
        else:
            self.play(self.pointer1.animate.move_to(self.cards2[i].get_critical_point(DOWN), UP),
                      self.pointer2.animate.move_to(self.cards2[j].get_critical_point(DOWN), UP))
        animations = []
        for k in range(start, end + 1):
            if i > mid:
                self.array[k] = self.temp[j]

                card = self.generateCard(self.temp[j], color=self.cards2[j][0].get_color()) \
                    .move_to(self.cards[k], DOWN)
                arrow = Arrow(start=self.cards2[j].get_critical_point(UP),
                              end=card.get_critical_point(DOWN),
                              buff=SMALL_BUFF,
                              stroke_width=2)
                self.play(self.pointer2.animate.move_to(self.cards2[j].get_critical_point(DOWN), UP))
                self.play(ShowCreationThenFadeOut(arrow),
                          ReplacementTransform(self.cards[k], card))
                j += 1
            elif j > end:
                self.array[k] = self.temp[i]
                card = self.generateCard(self.temp[i], color=self.cards2[i][0].get_color()) \
                    .move_to(self.cards[k], DOWN)
                if k == i:
                    direction1, direction2 = UP, DOWN
                else:
                    direction1, direction2 = UP + RIGHT, DOWN + LEFT
                arrow = Arrow(start=self.cards2[i].get_critical_point(direction1),
                              end=card.get_critical_point(direction2),
                              buff=SMALL_BUFF, stroke_width=2)
                self.play(self.pointer1.animate.move_to(self.cards2[i].get_critical_point(DOWN), UP))
                self.play(ShowCreationThenFadeOut(arrow),
                          ReplacementTransform(self.cards[k], card))
                i += 1
            elif self.temp[i] > self.temp[j]:
                self.array[k] = self.temp[j]
                card = self.generateCard(self.temp[j], color=self.cards2[j][0].get_color()) \
                    .move_to(self.cards[k], DOWN)
                if k == j:
                    direction1, direction2 = UP, DOWN
                else:
                    direction1, direction2 = UP + LEFT, DOWN + RIGHT
                arrow = Arrow(start=self.cards2[j].get_critical_point(direction1),
                              end=card.get_critical_point(direction2),
                              buff=SMALL_BUFF, stroke_width=2)
                self.play(self.pointer1.animate.move_to(self.cards2[i].get_critical_point(DOWN), UP),
                          self.pointer2.animate.move_to(self.cards2[j].get_critical_point(DOWN), UP))
                self.play(ShowCreationThenFadeOut(arrow),
                          ReplacementTransform(self.cards[k], card))
                j += 1
            else:
                self.array[k] = self.temp[i]
                card = self.generateCard(self.temp[i], color=self.cards2[i][0].get_color()) \
                    .move_to(self.cards[k], DOWN)
                if k == i:
                    direction1, direction2 = UP, DOWN
                else:
                    direction1, direction2 = UP + RIGHT, DOWN + LEFT
                arrow = Arrow(start=self.cards2[i].get_critical_point(direction1),
                              end=card.get_critical_point(direction2),
                              buff=SMALL_BUFF, stroke_width=2)
                self.play(self.pointer1.animate.move_to(self.cards2[i].get_critical_point(DOWN), UP),
                          self.pointer2.animate.move_to(self.cards2[j].get_critical_point(DOWN), UP))
                self.play(ShowCreationThenFadeOut(arrow),
                          ReplacementTransform(self.cards[k], card))
                i += 1
            self.cardGroup.remove(self.cards[k])
            self.cardGroup.add(card)
            self.cards[k] = card

    def addCode(self, code):
        if self.codeBlock == None:
            self.codeBlock = Code(code=code, language='python').to_edge(UP + LEFT)
            return Create(self.codeBlock)
        else:
            codeBlock = self.codeBlock
            self.codeBlock = Code(code='\n'.join([self.codeBlock.code_string, code]), language='python') \
                .to_edge(UP + LEFT)
            return ReplacementTransform(codeBlock, self.codeBlock)

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
            card2 = self.generateCard(self.temp[i], color=BLUE) \
                .move_to([base_x + i * CARD_SPACE, base_y, 0], aligned_edge=DOWN + LEFT)
            self.cards2.append(card2)
            self.cardGroup2.add(card2)
        self.cardGroup2.shift([0, -CARD_MAX_HEIGHT - MED_LARGE_BUFF, 0])
        return self.cardGroup

    def drawGrid(self):
        vGroup = VGroup()
        for i in range(int(-config.frame_x_radius), int(config.frame_x_radius)):
            if i == 0:
                line = Line([i, -config.frame_y_radius, 0], [i, config.frame_y_radius, 0],
                            stroke_opacity=1, color=RED, stroke_width=8)
                vGroup.add(line)

            else:
                vGroup.add(Line([i, -config.frame_y_radius, 0], [i, config.frame_y_radius, 0], stroke_opacity=1,
                                fill_opacity=1))
            # for k in np.arange(i + 0.5, i + 1, 0.5):
            #     vGroup.add(DashedLine([k, -config.frame_y_radius, 0], [k, config.frame_y_radius, 0],
            #                           stroke_opacity=1,
            #                           fill_opacity=1))
        for j in range(int(-config.frame_y_radius), int(config.frame_y_radius)):
            if j == 0:
                vGroup.add(Line([-config.frame_x_radius, j, 0], [config.frame_x_radius, j, 0],
                                stroke_width=8, color=RED))
            else:
                vGroup.add(Line([-config.frame_x_radius, j, 0], [config.frame_x_radius, j, 0],
                                stroke_opacity=1,
                                fill_opacity=1))
            # for k in np.arange(j + 0.5, j + 5, 0.5):
            #     vGroup.add(DashedLine([-config.frame_x_radius, k, 0], [config.frame_x_radius, k, 0],
            #                           stroke_opacity=1,
            #                           fill_opacity=1))
            self.add(vGroup)
