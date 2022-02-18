from BinaryHeap import *
from manim import *
import numpy as np
from my_ctex import my_ctex


class BinaryHeapScene(Scene):
    def construct(self):
        self.noteGroup = VGroup()
        title = Tex('二叉堆',
                    tex_template=TexTemplateLibrary.ctex, font_size=48).to_edge(UP)
        self.play(Create(title))
        note1 = Tex(r'二叉堆是一种有序的二叉树结构，树的每一个节点的值均大于它的两个\\'
                    r'子节点。通过二叉堆可以实现优先队列的基本操作，也是堆排序的基础。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft', font_size=28) \
            .next_to(title, DOWN) \
            .to_edge(LEFT, SMALL_BUFF)
        self.noteGroup.add(note1)
        self.play(Create(note1))

        group1 = VGroup()
        heap1 = BinaryHeap(self, depth=2)
        heap1.setData([1, 2, 3])
        # self.heap.top = [config.frame_x_radius - self.heap.width() / 2,
        #                  config.frame_y_radius-2*self.heap.radius, 0]
        heap1.createTree()
        heap1.treeGroup.next_to(title, DOWN).next_to(note1, RIGHT, buff=MED_LARGE_BUFF)
        self.play(Create(heap1.treeGroup))

        wrong = Text('×', color=RED).next_to(heap1.treeGroup, RIGHT)
        self.play(Create(wrong))

        heap2 = BinaryHeap(self, depth=2)
        heap2.setData([3, 2, 1])
        # self.heap.top = [config.frame_x_radius - self.heap.width() / 2,
        #                  config.frame_y_radius-2*self.heap.radius, 0]
        heap2.createTree()
        heap2.treeGroup.next_to(title, DOWN).next_to(wrong, RIGHT)
        self.play(Create(heap2.treeGroup))

        right = Text('√', color=GREEN).next_to(heap2.treeGroup, RIGHT)
        self.play(Create(right))
        group1.add(heap1.treeGroup, wrong, heap2.treeGroup, right)

        self.wait(2)

        note2 = Tex(r'二叉树可以用数组来保存，首元素为二叉树的根节点，它的两个叶子节点\\'
                    r'的位置分别为1和2，随后位置1的叶子节点的位置为3和4，以此类推。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft', font_size=28) \
            .next_to(note1, DOWN).to_edge(LEFT, SMALL_BUFF)
        self.noteGroup.add(note2)
        self.play(Create(note2))

        heap3 = BinaryHeap(self, depth=3)
        heap3.setData([6, 3, 5, 2, 1, 4])
        # self.heap.top = [config.frame_x_radius - self.heap.width() / 2,
        #                  config.frame_y_radius-2*self.heap.radius, 0]
        heap3.createTree()
        heap3.treeGroup.next_to(group1, DOWN)
        heap3.createCards(None, 0, 0)
        heap3.cardGroup.next_to(heap3.treeGroup, DOWN)
        self.play(Create(heap3.treeGroup), Create(heap3.cardGroup))

        self.wait(2)

        note3 = Tex(r'向二叉堆的末端插入新的节点，可能会破坏二叉堆的有序性，这时，需要\\'
                    r'对新加入的元素进行有序化(上浮)，直到二叉堆重新有序。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft', font_size=28) \
            .next_to(note2, DOWN).to_edge(LEFT, SMALL_BUFF)
        self.noteGroup.add(note3)
        self.play(Create(note3))

        heap4 = BinaryHeap(self, depth=3)
        heap4.setData([3, 2, 1])
        # self.heap.top = [config.frame_x_radius - self.heap.width() / 2,
        #                  config.frame_y_radius-2*self.heap.radius, 0]
        heap4.createTree()
        heap4.treeGroup.next_to(heap3.cardGroup, DOWN)
        heap4.createCards(None)
        heap4.cardGroup.next_to(heap4.treeGroup, DOWN,
                                buff=heap4.treeHeight() - heap4.treeGroup.height + 0.25) \
            .to_edge(RIGHT, buff=CARD_SPACE * 4)

        self.play(Create(heap4.treeGroup), Create(heap4.cardGroup))
        self.wait(1)

        heap4.insert(6, True)
        heap4.insert(5, True)
        heap4.insert(4, True)
        heap4.insert(7, True)

        self.wait(2)

        note4 = Tex(r'当从二叉堆顶端删除一个节点时，可以将末端叶子换到顶端，并进行下沉\\'
                    r'操作，从而恢复二叉堆的有序性。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft', font_size=28) \
            .next_to(note3, DOWN).to_edge(LEFT, SMALL_BUFF)
        self.noteGroup.add(note4)
        self.play(Create(note4))

        heap4.delMax(True)
        self.wait(1)
        heap4.delMax(True)

        self.wait(2)

        note5 = Tex(r'将一个无序的二叉树有序化，只需对位置从$\frac{N}{2}-1$到$0$的元素进行下沉\\'
                    r'操作即可，这是因为没有子节点的叶子是不需要下沉的，因此可以省去这\\'
                    r'些操作。',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft', font_size=28) \
            .next_to(note4, DOWN).to_edge(LEFT, SMALL_BUFF)
        self.noteGroup.add(note5)
        self.play(Create(note5))

        heap5 = BinaryHeap(self, depth=3)
        heap5.setData([1, 2, 3, 4, 5, 6, 7])
        # self.heap.top = [config.frame_x_radius - self.heap.width() / 2,
        #                  config.frame_y_radius-2*self.heap.radius, 0]
        heap5.createTree()
        heap5.createCards(None)
        heap5.treeGroup.next_to(heap3.cardGroup, DOWN)
        heap5.cardGroup.next_to(heap4.treeGroup, DOWN)
        self.play(ReplacementTransform(heap4.treeGroup, heap5.treeGroup),
                  ReplacementTransform(heap4.cardGroup, heap5.cardGroup))

        self.wait(1)
        heap5.tidy(True)
        self.wait(2)


class HeapSortScene(Scene):
    def construct(self):
        self.section = VGroup()
        title = Tex('堆排序',
                    tex_template=TexTemplateLibrary.ctex, font_size=48).to_edge(UP)
        self.play(Create(title))

        note1 = Tex(r'接上回书，通过二叉堆可以实现堆排序，对无序的数组进行堆有序化后，'
                    r'并没有建立完全有序的数组，堆有序$\ne$有序，在建立二叉堆之后，可以'
                    r'通过不断地将顶部的最大值与末端叶子进行交换，随后对交换到顶部的元素'
                    r'进行下沉操作，这次下沉操作将不考虑已经交换到末端的最大值，末端最大值'
                    r'的位置已经固定，如此循环，直到最后只剩一个顶部元素为止，排序结束，此时，'
                    r'数组成为从小到大排序的有序数组。',
                    tex_template=my_ctex,
                    tex_environment='flushleft', font_size=30) \
            .next_to(title, DOWN) \
            .to_edge(LEFT, MED_SMALL_BUFF)
        self.section.add(note1)
        self.play(Create(note1))
        self.wait(1)
        heap3 = BinaryHeap(self, depth=4, font_size=28)
        heap3.setData([33, 11, 22, 55, 66, 88, 99, 77, 33])
        # self.heap.top = [config.frame_x_radius - self.heap.width() / 2,
        #                  config.frame_y_radius-2*self.heap.radius, 0]
        heap3.createTree(repeat_val=33)
        heap3.treeGroup.next_to(note1, DOWN)
        heap3.createCards(33, 0, 0)
        heap3.cardGroup.next_to(heap3.treeGroup, DOWN)
        self.section.add(heap3.treeGroup)
        self.section.add(heap3.cardGroup)
        self.play(Create(heap3.treeGroup), Create(heap3.cardGroup))
        self.showLegend(note1)
        step1 = Tex('第一步：堆有序化',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft', font_size=28)\
            .next_to(note1, DOWN)\
            .to_edge(LEFT)
        self.play(Create(step1))
        self.wait(1)
        heap3.tidy(True)
        self.wait(1)
        step2 = Tex('第二步：下沉排序',
                    tex_template=TexTemplateLibrary.ctex,
                    tex_environment='flushleft', font_size=28) \
            .next_to(note1, DOWN) \
            .to_edge(LEFT)
        self.play(ReplacementTransform(step1, step2))
        self.wait(1)
        heap3.heapSort(True)
        self.wait(2)
        self.play(Uncreate(note1))
        note2 = Tex(r'堆排序是一种不稳定的排序算法，两个33在排序前后的位置发生了变化，'
                    r'堆排序的时间复杂度为$n\text{log}_2n$,在最差的情况下，即每次下沉'
                    r'操作均需要遍历所有层也只需约$n\text{log}_2n$次比较。但是，堆排序'
                    r'比较时很少会和相邻的元素进行比较，因此，缓存未命中的几率远高于其他'
                    r'在相邻元素间进行比较的算法，如快速排序，归并排序等，因此会极大地影响'
                    r'速度。',
                    tex_template=my_ctex,
                    tex_environment='flushleft', font_size=28) \
            .next_to(title, DOWN) \
            .to_edge(LEFT, MED_SMALL_BUFF)
        self.section.add(note2)
        self.play(Create(note2))
        self.wait(2)


    def showLegend(self, down):
        self.legendGroup = VGroup()
        arrRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5, color=BLUE)
        arrLabel = Text('未排序数组', font_size=15).next_to(arrRect, RIGHT)
        arrLegend = VGroup(arrRect, arrLabel)\
            .next_to(down, DOWN, MED_SMALL_BUFF)\
            .to_edge(RIGHT, MED_LARGE_BUFF)

        finishedRect = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.5,
                                     color=GREY).next_to(arrRect, DOWN)
        finishedLabel = Text('已确定位置', font_size=15).next_to(finishedRect, RIGHT)
        finishedLegend = VGroup(finishedRect, finishedLabel)

        repeatRect1 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                        fill_color=GREEN, fill_opacity=1)
        repeatRect2 = RoundedRectangle(corner_radius=0, width=0.25, height=0.5,
                                        fill_color=PINK, fill_opacity=1).next_to(repeatRect1, RIGHT, 0)
        repeatRect = VGroup(repeatRect1, repeatRect2).next_to(finishedRect, DOWN)
        repeatLabel = Text('相同值', font_size=15).next_to(repeatRect, RIGHT)
        repeatLegend = VGroup(repeatRect, repeatLabel)

        self.legendGroup.add(arrLegend, finishedLegend, repeatLegend)

        self.play(Create(arrLegend), Create(finishedLegend), Create(repeatLegend))
