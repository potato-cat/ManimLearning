from sympy import Shi
from sympy.physics.secondquant import CreateBoson

from manim import *
import numpy as np

FRAME_WIDTH = config.frame_width
FRAME_HEIGH = config.frame_height

FRAME_X_RADIUS = config.frame_x_radius
FRAME_Y_RADIUS = config.frame_y_radius



class TowerOfHanoiScene(Scene):
    def construct(self):
        self.diskes1 = []
        self.diskes2 = []
        self.diskes3 = []
        self.diskes = [self.diskes1, self.diskes2, self.diskes3]
        right = Text('√', color=GREEN)
        wrong = Text('×', color=RED)
        textGroup = VGroup()
        self.hanoi = VGroup()

        # self.drawGrid()
        # 标题
        intro_words = Text('汉诺塔问题')
        intro_words.to_edge(UP)
        self.play(Write(intro_words))
        self.drawPin()
        # 介绍
        hanoi_intro = Tex(
            '汉诺塔是一个著名的数学问题，起源于古印度，由三根柱子以及n个碟片构成',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='{flushleft}').scale(0.6)
        textGroup.add(hanoi_intro)
        hanoi_intro.next_to(intro_words, DOWN).to_edge(LEFT, 0)
        self.play(Write(hanoi_intro, run_time=1))
        # 规则
        self.setHanoi(6)
        hanoi_rule = Tex(
            '汉诺塔的规则是每次只能移动最上面的一个碟片，且大的碟片必须位于小的碟片下面',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft').scale(0.6)
        textGroup.add(hanoi_rule)
        hanoi_rule.next_to(hanoi_intro, DOWN)
        hanoi_rule.move_to([-FRAME_X_RADIUS + hanoi_rule.width / 2, hanoi_rule.get_y(), 0])
        self.play(Write(hanoi_rule, run_time=1))
        self.moveDisk(0, 1)
        self.moveDisk(0, 2)
        self.moveDisk(1, 2)
        self.play(Write(right.to_edge(RIGHT)))
        self.wait(1)
        #
        self.clearHanoi()
        self.remove(right)
        self.setHanoi(6)
        self.moveDisk(0, 1)
        self.moveDisk(0, 1)
        self.play(Write(wrong.to_edge(RIGHT)))
        #
        self.wait(1)
        self.remove(wrong)

        hanoi_solve = Tex(
            '汉诺塔是一个典型的递归问题，因为它可以分解为自身的更简单的情况，复杂度降低',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft').scale(0.6)
        textGroup.add(hanoi_solve)
        hanoi_solve.next_to(hanoi_rule, DOWN)
        hanoi_solve.move_to([-FRAME_X_RADIUS + hanoi_solve.width / 2, hanoi_solve.get_y(), 0])
        self.play(Write(hanoi_solve, run_time=1))
        #
        self.wait(1)
        self.play(Uncreate(textGroup))
        self.clearHanoi()

        n1 = Tex(
            '首先来看$n=1$时的情况，显然，只需要直接移动即可',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft').scale(0.6)
        n1.next_to(intro_words, DOWN).to_edge(LEFT, 0)
        self.play(Write(n1))
        self.setHanoi(1)
        self.solveHanoi(1, 0, 2)

        self.wait(1)
        self.play(Uncreate(n1))
        self.clearHanoi()
        n2 = Tex(
            '接下来看n=2时的情况，显然，也只需要简单的移动即可',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft').scale(0.6)
        n2.next_to(intro_words, DOWN).to_edge(LEFT, 0)
        self.play(Write(n2))
        self.setHanoi(2)
        self.solveHanoi(2, 0, 2)

        self.wait(1)
        self.play(Uncreate(n2))
        textGroup = VGroup()
        self.clearHanoi()
        n3 = Tex(
            '接下来看$n=3$时的情况，此时，问题可以分解为$n=2$与$n=1$两个问题',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft').scale(0.6)
        textGroup.add(n3)
        n3.next_to(intro_words, DOWN).to_edge(LEFT, 0)
        self.play(Write(n3))

        hanoi3 = Tex('Hanoi(3, 0, 2)').scale(0.6).next_to(n3, DOWN).to_edge(LEFT)
        textGroup.add(hanoi3)
        self.play(Write(hanoi3))
        self.setHanoi(3)

        arrow1 = Arrow().set_length(1).next_to(hanoi3, RIGHT)
        textGroup.add(arrow1)
        self.play(Write(arrow1))

        hanoi21 = Tex('Hanoi(2, 0, 1)').scale(0.6).next_to(arrow1, RIGHT)
        textGroup.add(hanoi21)
        self.play(Write(hanoi21))
        self.highlight(2, 0, 1)

        arrow2 = Arrow().set_length(1).next_to(hanoi21, RIGHT)
        textGroup.add(arrow2)
        self.play(Write(arrow2))

        hanoi11 = Tex('Hanoi(1, 0, 2)').scale(0.6).next_to(arrow2, RIGHT)
        textGroup.add(hanoi11)
        self.play(Write(hanoi11))
        self.highlight(1, 0, 2)

        arrow3 = Arrow().set_length(1).next_to(hanoi11, RIGHT)
        textGroup.add(arrow3)
        self.play(Write(arrow3))

        hanoi22 = Tex('Hanoi(2, 1, 2)').scale(0.6).next_to(arrow3, RIGHT)
        textGroup.add(hanoi22)
        self.play(Write(hanoi22))
        self.highlight(2, 1, 2)


        self.wait(2)
        self.clearHanoi()
        self.setHanoi(3)
        self.solveHanoi(3, 0, 2)
        #
        self.wait(2)
        self.play(Uncreate(textGroup))
        self.clearHanoi()
        textGroup = VGroup()
        n4 = Tex(
            '接下来看$n=4$时的情况,',
            tex_environment='flushleft',
            tex_template=TexTemplateLibrary.ctex).scale(0.6)
        textGroup.add(n4)
        n4.next_to(intro_words, DOWN).to_edge(LEFT, 0)
        n4.move_to([-FRAME_X_RADIUS + n4.width / 2, n4.get_y(), 0])
        self.play(Write(n4))
        self.setHanoi(4)
        self.solveHanoi(4, 0, 2)
        countTex = Tex(
            '一共移动15次完成。',
            tex_environment='flushleft',
            tex_template=TexTemplateLibrary.ctex).scale(0.6)
        textGroup.add(countTex)
        countTex.next_to(n4, RIGHT)
        self.play(Write(countTex))
        self.wait(1)

        self.play(Uncreate(textGroup))
        textGroup = VGroup()
        self.clearHanoi()
        n5 = Tex(
            '综上,汉诺塔的执行时间随阶数升高会指数爆炸,根据分解可以得到$T(n)=2T(n-1)+T(1)$,'
            '得到汉诺塔的执行步数为$2^n-1$，其中，n为汉诺塔的阶数,'
            '可得汉诺塔时间复杂度$O(n)=2^n$。',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft'
        ).scale(0.6)
        textGroup.add(n5)
        n5.next_to(intro_words, DOWN).to_edge(LEFT, 0)
        n5.move_to([-FRAME_X_RADIUS + n5.width / 2, n5.get_y(), 0])
        self.play(Write(n5))
        n6 = Tex(
            '传说，大梵天创造世界时，第一根柱子上面放了64枚碟片，'
            '当碟片移动结束时，世界将会毁灭，那么64枚碟片需要多久呢？按上面的计算共需移动$2^{64}-1$次。',
            tex_template=TexTemplateLibrary.ctex,
            tex_environment='flushleft'
        ).scale(0.6)
        textGroup.add(n6)
        n6.next_to(n5, DOWN)
        self.play(Write(n6))
        self.wait(4)

        self.play(Uncreate(textGroup))
        n7 = Tex(
            '接下来感受无聊的指数爆炸吧！！！',
            tex_environment='flushleft',
            tex_template=TexTemplateLibrary.ctex).scale(0.6)
        textGroup.add(n7)
        n7.next_to(intro_words, DOWN).to_edge(LEFT, 0)
        n7.move_to([-FRAME_X_RADIUS + n7.width / 2, n7.get_y(), 0])
        self.play(Write(n7))
        self.setHanoi(6)
        self.solveHanoi(6, 0, 2)
        self.wait(1)
        self.clear()
        self.wait(1)


    def highlight(self, order, src, dest):
        diskes = [self.diskes[src].pop(-1) for i in range(order)]
        vgroup = VGroup(*diskes)
        self.play(vgroup.animate.set_fill(random_bright_color()))
        path = VGroup()
        vertices = [vgroup.get_center(), [vgroup.get_center()[0], 1, 0],
                    [-FRAME_WIDTH / 3 + dest * FRAME_WIDTH / 3, 1, 0],
                    [-FRAME_WIDTH / 3 + dest * FRAME_WIDTH / 3,
                     -FRAME_Y_RADIUS + 0.5 + (len(self.diskes[dest])+len(diskes)/2)*0.5, 0]]
        path.set_points_as_corners(vertices)
        self.play(MoveAlongPath(vgroup, path))
        self.diskes[dest].extend(diskes)

    def solveHanoi(self, order, src, dest):
        # 问题拆分
        temp = ({0, 1, 2} - {src, dest}).pop()
        if order == 1:
            self.moveDisk(src, dest)
        elif order == 2:
            self.moveDisk(src, temp)
            self.moveDisk(src, dest)
            self.moveDisk(temp, dest)
        else:
            self.solveHanoi(order-1, src, temp)
            self.solveHanoi(1, src, dest)
            self.solveHanoi(order-1, temp, dest)

    def moveDisk(self, src, dest):
        disk = self.diskes[src].pop(-1)
        self.diskes[dest].append(disk)
        path = VGroup()
        vertices = [disk.get_center(), [disk.get_center()[0], 1, 0],
                      [-FRAME_WIDTH/3+dest*FRAME_WIDTH/3, 1, 0],
                      [-FRAME_WIDTH/3+dest*FRAME_WIDTH/3,
                            -FRAME_Y_RADIUS + 0.75 + (len(self.diskes[dest])-1)*0.5, 0]]
        path.set_points_as_corners(vertices)
        self.play(MoveAlongPath(disk, path))

    def drawPin(self):
        # 竖线
        self.add(Line([-FRAME_WIDTH / 3, -FRAME_Y_RADIUS + 0.5, 0], [-FRAME_WIDTH / 3, 0, 0]))
        i = -FRAME_X_RADIUS + 0.5
        self.add(Line([-FRAME_X_RADIUS, -FRAME_Y_RADIUS + 0.5, 0],
                            [-FRAME_WIDTH / 6, -FRAME_Y_RADIUS + 0.5, 0]))
        while i < -FRAME_WIDTH / 6:
            self.add(Line([i, -FRAME_Y_RADIUS + 0.5, 0], [i - 0.5, -FRAME_Y_RADIUS, 0]))
            i += 0.5
        # 竖线
        self.add(Line([0, -FRAME_Y_RADIUS + 0.5, 0], [0, 0, 0]))
        i = -FRAME_X_RADIUS + FRAME_WIDTH / 3 + 0.5
        self.add(Line([-FRAME_X_RADIUS + FRAME_WIDTH / 3, -FRAME_Y_RADIUS + 0.5, 0],
                            [FRAME_WIDTH / 6, -FRAME_Y_RADIUS + 0.5, 0]))
        while i < FRAME_WIDTH / 6:
            self.add(Line([i, -FRAME_Y_RADIUS + 0.5, 0], [i - 0.5, -FRAME_Y_RADIUS, 0]))
            i += 0.5
        # 竖线
        self.add(Line([FRAME_WIDTH / 3, -FRAME_Y_RADIUS + 0.5, 0], [FRAME_WIDTH / 3, 0, 0]))
        i = -FRAME_X_RADIUS + FRAME_WIDTH / 3 * 2 + 0.5
        self.add(Line([FRAME_WIDTH / 6, -FRAME_Y_RADIUS + 0.5, 0],
                            [FRAME_X_RADIUS, -FRAME_Y_RADIUS + 0.5, 0]))
        while i < FRAME_X_RADIUS:
            self.add(Line([i, -FRAME_Y_RADIUS + 0.5, 0], [i - 0.5, -FRAME_Y_RADIUS, 0]))
            i += 0.5

    def clearHanoi(self):
        self.diskes1.clear()
        self.diskes2.clear()
        self.diskes3.clear()
        self.play(Uncreate(self.hanoi))

    def setHanoi(self, order: int) -> None:
        for i in range(order):
            disk = RoundedRectangle(fill_opacity=1, color=PINK, stroke_color=WHITE,
                                    width=(FRAME_WIDTH*9/10)/3/6*(order-i), height=0.5, corner_radius=0.25)
            disk.move_to([-FRAME_WIDTH/3, -FRAME_Y_RADIUS + 0.75+i*0.5, 0])
            self.hanoi.add(disk)
            self.diskes1.append(disk)
        self.play(Create(self.hanoi))

    def drawGrid(self):
        # for i in range(int(-FRAME_X_RADIUS), int(FRAME_X_RADIUS)):
        #     if i == 0:
        #         line=Line([i, -FRAME_Y_RADIUS, 0], [i, FRAME_Y_RADIUS, 0],
        #              stroke_opacity=1, color=RED, stroke_width=8)
        #         self.add(line)
        #
        #     else:
        #         self.add(Line([i, -FRAME_Y_RADIUS, 0], [i, FRAME_Y_RADIUS, 0], stroke_opacity=1, fill_opacity=1))
        # for j in range(int(-FRAME_Y_RADIUS), int(FRAME_Y_RADIUS)):
        #     if j == 0:
        #         self.add(Line([-FRAME_X_RADIUS, j, 0], [FRAME_X_RADIUS, j, 0],
        #                       stroke_width=8, color=RED))
        #     else:
        #         self.add(Line([-FRAME_X_RADIUS, j, 0], [FRAME_X_RADIUS, j, 0], stroke_opacity=1, fill_opacity=1))
        self.add(Line([-FRAME_WIDTH/6, -FRAME_Y_RADIUS, 0], [-FRAME_WIDTH/6, FRAME_Y_RADIUS, 0],
                      stroke_opacity=1, fill_opacity=1))
        self.add(Line([FRAME_WIDTH / 6, -FRAME_Y_RADIUS, 0], [FRAME_WIDTH / 6, FRAME_Y_RADIUS, 0],
                      stroke_opacity=1, fill_opacity=1))
