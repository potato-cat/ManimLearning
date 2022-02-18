from manim import *
from my_movement import *
import numpy as np

CARD_WIDTH = 0.4
CARD_SPACE = 0.6
CARD_MAX_HEIGHT = 2
CARD_MIN_HEIGHT = 0.5


class BinaryHeap:
    def __init__(self, scene, radius=0.2, depth=2, buff=0.2, top=[0, 0, 0], font_size=20):
        self.data = []
        self.tree = []
        self.cards = []
        self.lines = [None]
        self.treeGroup = VGroup()
        self.cardGroup = VGroup()
        self.radius = radius
        self.depth = depth
        self.buff = buff
        self.top = top
        self.scene = scene
        self.fontSize = font_size
        self.cardColor = BLUE

    def setData(self, data: []):
        self.data = data

    def createCards(self, repeat_val, base_x=0, base_y=0.5):
        initPos = base_x
        color_index = 0
        self.baseX = base_x
        self.baseY = base_y
        for i, v in enumerate(self.data):
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
                                    color=fillColor) \
                .move_to([initPos + i * CARD_SPACE, base_y, 0], aligned_edge=DOWN + LEFT)
            num = DecimalNumber(v, num_decimal_places=0, font_size=self.fontSize) \
                .move_to(rect.get_center())
            card.add(rect, num)
            self.cards.append(card)
            self.cardGroup.add(card)
        return self.cardGroup

    def createTree(self, repeat_val):
        # 确定各叶子的位置
        color_index = 0
        for i in range(len(self.data)):
            layer = int(np.log2(i + 1)) + 1
            if layer == 1:
                pos = self.top
            else:
                root = self.tree[int(np.floor((i + 1) / 2)) - 1]
                rPos = root[0].get_center()
                if i % 2 == 1:
                    pos = rPos + \
                          [-2 ** (self.depth - layer) * (self.radius + self.buff / 2),
                           -(self.buff + self.radius * 2), 0]
                    logger.info('%d:%d, %f' % (i, layer, -2 ** (self.depth - layer) * (self.radius + self.buff / 2)))
                else:
                    pos = root[0].get_center() + \
                          [2 ** (self.depth - layer) * (self.radius + self.buff / 2),
                           -(self.buff + self.radius * 2), 0]
                    logger.info('%d:%d, %f' % (i, layer, 2 ** (self.depth - layer) * (self.radius + self.buff / 2)))
                slope = (pos[0] - rPos[0]) / (pos[1] - rPos[1])
                y1 = rPos[1] - self.radius / np.sqrt(slope ** 2 + 1)
                x1 = (y1 - rPos[1]) * slope + rPos[0]
                y2 = pos[1] + self.radius / np.sqrt(slope ** 2 + 1)
                x2 = (y2 - pos[1]) * slope + pos[0]
                line = Line(start=[x1, y1, 0], end=[x2, y2, 0])
                self.lines.append(line)
                self.treeGroup.add(line)
            if self.data[i] == repeat_val:
                if color_index == 0:
                    fillColor = PINK
                    color_index = 1
                else:
                    fillColor = GREEN
            else:
                fillColor = BLUE
            leaf = VGroup()
            circle = Circle(self.radius, fillColor).move_to(pos)
            num = DecimalNumber(self.data[i], 0, font_size=self.fontSize).move_to(circle)
            leaf.add(circle, num)
            self.treeGroup.add(leaf)
            self.tree.append(leaf)

    def swap(self, i, j, include_card=False):
        if i == j:
            return
        self.data[i], self.data[j] = self.data[j], self.data[i]
        a, b = min(i, j), max(i, j)
        pos1 = self.tree[a].get_center()
        pos2 = self.tree[b].get_center()
        center = (pos1 + pos2) / 2
        radius = np.linalg.norm(pos1 - center)
        logger.info("radius:%f, %f" % (radius, np.linalg.norm(pos1 - pos2) / 2))
        angle = np.arctan2(pos1[1] - pos2[1], pos1[0] - pos2[0])
        logger.info("angle:%f" % angle)
        path1 = Arc(radius, 0, PI).move_to(center, aligned_edge=DOWN).rotate(angle, about_point=center)
        path2 = Arc(radius, PI, PI).move_to(center, aligned_edge=UP).rotate(angle, about_point=center)
        if include_card:
            path3 = Arc(abs(j - i) * CARD_SPACE / 2, PI, -PI)
            path3.move_to((self.cards[i].get_critical_point(DOWN) + self.cards[j].get_critical_point(DOWN)) / 2,
                          aligned_edge=DOWN)
            path4 = Arc(abs(j - i) * CARD_SPACE / 2, 0, PI)
            path4.move_to((self.cards[i].get_critical_point(DOWN) + self.cards[j].get_critical_point(DOWN)) / 2,
                          aligned_edge=DOWN)
            self.scene.play(MoveAlongPath(self.tree[a], path1),
                            MoveAlongPath(self.tree[b], path2),
                            MyMoveAlongPath(self.cards[a], path3, aligned_edge=DOWN),
                            MyMoveAlongPath(self.cards[b], path4, aligned_edge=DOWN))
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        else:
            self.scene.play(MoveAlongPath(self.tree[a], path1),
                            MoveAlongPath(self.tree[b], path2))
        self.tree[i], self.tree[j] = self.tree[j], self.tree[i]

    def sink(self, k, N, include_card=False):
        while 2 * (k + 1) - 1 < N:
            j = 2 * (k + 1) - 1  # 左叶子
            # 右叶子更大
            if j + 1 < N and self.data[j] < self.data[j + 1]:
                j += 1
            if self.data[k] >= self.data[j]:
                break
            self.swap(k, j, include_card)
            self.scene.wait(0.5)
            k = j

    def swim(self, k, include_card=False):
        j = int((k + 1) / 2) - 1  # 爸爸
        while j >= 0 and self.data[k] > self.data[j]:
            self.swap(k, j, include_card)
            k = j
            j = int((k + 1) / 2) - 1

    def tidy(self, include_card=False):
        i = int(len(self.data) / 2) - 1
        while i >= 0:
            self.sink(i, len(self.data), include_card)
            i -= 1

    def insert(self, v, include_card=False):
        self.data.append(v)
        i = len(self.data) - 1
        layer = int(np.log2(i + 1)) + 1
        if layer == 1:
            pos = self.top
            root = None
        else:
            root = self.tree[int(np.floor((i + 1) / 2)) - 1]
            rPos = root[0].get_center()
            if i % 2 == 1:
                pos = rPos + \
                      [-2 ** (self.depth - layer) * (self.radius + self.buff / 2),
                       -(self.buff + self.radius * 2), 0]
                logger.info('%d:%d, %f' % (i, layer, -2 ** (self.depth - layer) * (self.radius + self.buff / 2)))
            else:
                pos = root[0].get_center() + \
                      [2 ** (self.depth - layer) * (self.radius + self.buff / 2),
                       -(self.buff + self.radius * 2), 0]
                logger.info('%d:%d, %f' % (i, layer, 2 ** (self.depth - layer) * (self.radius + self.buff / 2)))
            slope = (pos[0] - rPos[0]) / (pos[1] - rPos[1])
            y1 = rPos[1] - self.radius / np.sqrt(slope ** 2 + 1)
            x1 = (y1 - rPos[1]) * slope + rPos[0]
            y2 = pos[1] + self.radius / np.sqrt(slope ** 2 + 1)
            x2 = (y2 - pos[1]) * slope + pos[0]
            line = Line(start=[x1, y1, 0], end=[x2, y2, 0])
            self.lines.append(line)
            self.treeGroup.add(line)
        leaf = VGroup()
        circle = Circle(self.radius, BLUE).move_to(pos)
        num = DecimalNumber(self.data[i], 0, font_size=self.fontSize).move_to(circle)
        leaf.add(circle, num)
        if include_card:
            card = VGroup()
            rect = RoundedRectangle(0.1, width=CARD_WIDTH,
                                    height=CARD_MIN_HEIGHT + (v - 10) / 90 * (CARD_MAX_HEIGHT - CARD_MIN_HEIGHT),
                                    color=BLUE) \
                .next_to(self.cards[-1], RIGHT, CARD_SPACE - CARD_WIDTH, aligned_edge=DOWN)
            num = DecimalNumber(v, num_decimal_places=0, font_size=self.fontSize) \
                .move_to(rect.get_center())
            card.add(rect, num)
            self.cards.append(card)
            self.cardGroup.add(card)
            self.scene.play(Create(leaf), Create(card))
        else:
            self.scene.play(Create(leaf))
        self.treeGroup.add(leaf)
        self.tree.append(leaf)

        self.scene.wait(1)
        self.swim(len(self.data) - 1, include_card)

    def delMax(self, include_card=False):
        if len(self.data) == 1:
            v = self.data.pop(-0)
            leaf = self.tree.pop(0)
            if include_card:
                card = self.cards.pop(0)
                self.scene.play(FadeOut(leaf), FadeOut(card))
                self.treeGroup.remove(leaf)
                self.cardGroup.remove(card)
            else:
                self.scene.play(FadeOut(leaf))
                self.treeGroup.remove(leaf)
            return

        v = self.data.pop(-1)
        self.data[0] = v
        self.scene.play(FadeToColor(self.tree[0], RED),
                        FadeToColor(self.cards[0], RED))
        self.scene.wait(1)
        leaf = self.tree.pop(-1)
        pos2 = leaf.get_center()
        pos1 = self.tree[0].get_center()
        center = (pos1 + pos2) / 2
        radius = np.linalg.norm(pos1 - center)
        angle = np.arctan2(pos1[1] - pos2[1], pos1[0] - pos2[0])
        path2 = Arc(radius, PI, PI).move_to(center, aligned_edge=UP).rotate(angle, about_point=center)

        if include_card:
            card = self.cards.pop(-1)
            self.scene.play(FadeOut(self.cards[0]), FadeOut(self.tree[0]))
            self.scene.wait(1)
            path4 = Arc(len(self.cards) * CARD_SPACE / 2, 0, PI)
            path4.move_to((self.cards[0].get_critical_point(DOWN) + card.get_critical_point(DOWN)) / 2,
                          aligned_edge=DOWN)
            self.scene.play(MoveAlongPath(leaf, path2),
                            MyMoveAlongPath(card, path4, aligned_edge=DOWN))
            self.cardGroup.remove(self.cards[0])
            self.cards[0] = card

        else:
            self.scene.play(FadeOut(leaf))
            self.scene.wait(1)
            self.scene.play(MoveAlongPath(leaf, path2))

        self.treeGroup.remove(self.tree[0])
        line = self.lines.pop(-1)
        self.scene.remove(line)
        self.treeGroup.remove(line)
        self.tree[0] = leaf
        self.scene.wait(1)
        self.sink(0, len(self.tree), include_card)

    def heapSort(self, include_card=False):
        N = len(self.data) - 1
        while N > 0:
            self.swap(0, N, include_card)
            self.scene.play(FadeToColor(self.cards[N][0], GREY),
                            FadeToColor(self.tree[N][0], GREY))
            self.scene.wait(1)
            self.sink(0, N, include_card)
            self.scene.wait(1)
            N -= 1
        self.scene.play(FadeToColor(self.cards[N][0], GREY),
                        FadeToColor(self.tree[N][0], GREY))

    def treeWidth(self):
        return 2 ** (self.depth - 1) * (2 * self.radius + self.buff) - self.buff

    def treeHeight(self):
        return self.depth * (2 * self.radius + self.buff) - self.buff
