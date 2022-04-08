from manim import *
from scenes.SearchTable import SearchTable
from scenes.my_ctex import my_ctex
from widgets.scene import MScene
from widgets.ZCurveArrow import ZCurveArrow
from widgets.Struct import Struct

RUN_TIME = 0.5


class SearchTableScene(MScene):
    def construct(self):
        # self.drawGrid()
        svg = SVGMobject('assets/dog3.svg', color=BLACK, fill_opacity=1, stroke_opacity=0, height=1).to_edge(LEFT + UP,
                                                                                                             buff=SMALL_BUFF)
        self.add(svg)
        self.title = Tex('无序查找表',
                         tex_template=my_ctex(), font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.play(Create(self.title))
        self.note1 = Tex(r'生活中我们常会遇到这样的问题，想要从一堆数据中找到我们需要的，比如查字典，或者是从表格中找数据，这些都可以抽象为'
                         r'一个查找操作，算法中被称为查找表。\\'
                         r'无序查找表是查找表中最基础的一种，它基于链表实现，不对键值进行排序,因此，每次查找都要对整个表遍历直到找到相应的key值，'
                         r'得益于链表的特性,当加入一个表中没有的键值对时,时间复杂度仅为$O(1)$,但更新键值对时,还是需要遍历整个表的.',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))
        self.note2 = Tex(r'链表的基本单元(C语言中用结构体表示)包含一个存放下一个基本单元地址的元素,这样,通过这个地址,我们可以找到下一个基本单元,如此往复,实现对整个'
                         r'链表的访问.',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note1, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note2))
        self.note3 = Tex(r'如下图,是一个基本单元的示意图,',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note2, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note3))

        self.note4 = Tex(r'下面我们构造一个基本元素,以水果个数统计表为例,',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note3, RIGHT, 0)

        self.note5 = Tex(r'此时,首元素的地址指向为NULL,这时,我们新增一个元素,将其地址指向设为首个元素.',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note4, DOWN, MED_SMALL_BUFF) \
            .to_edge(LEFT, MED_SMALL_BUFF)

        s1 = Struct('UNIT', {'key': 'key', 'val': 'value'}, 'addr').next_to(self.note5, DOWN).to_edge(LEFT)
        self.play(Create(s1))

        self.play(Create(self.note4))

        s2 = Struct('Fruit1', {'key': 'apple', 'val': 2}, 'NULL').next_to(s1, RIGHT, LARGE_BUFF)
        self.play(Create(s2))

        self.play(Create(self.note5))

        s3 = Struct('Fruit2', {'key': 'banana', 'val': 5}, r'\&Fruit1').next_to(s2, RIGHT, MED_LARGE_BUFF)
        line1 = ZCurveArrow(s3.getPrevPoint(), s2.getCurPoint(), max_tip_length_to_length_ratio=0.1, stroke_width=2,
                            tip_length=0.2)
        self.play(Create(line1))
        self.play(Create(s3))

        self.note6 = Tex(r'以此类推.',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.note5, RIGHT, 0)
        self.play(Create(self.note6))

        s4 = Struct('Fruit3', {'key': 'pear', 'val': 3}, r'\&Fruit2').next_to(s3, RIGHT, MED_LARGE_BUFF)
        line2 = ZCurveArrow(s4.getPrevPoint(), s3.getCurPoint(), max_tip_length_to_length_ratio=0.1, stroke_width=2,
                            tip_length=0.2)
        self.play(Create(line2))
        self.play(Create(s4))

        s5 = Struct('Fruit4', {'key': 'peach', 'val': 6}, r'\&Fruit3').next_to(s4, RIGHT, MED_LARGE_BUFF)
        line3 = ZCurveArrow(s5.getPrevPoint(), s4.getCurPoint(), max_tip_length_to_length_ratio=0.1, stroke_width=2,
                            tip_length=0.2)
        self.play(Create(line3))
        self.play(Create(s5))

        self.play(Uncreate(self.note1), Uncreate(self.note2), Uncreate(self.note3), Uncreate(self.note4),
                  Uncreate(self.note5), Uncreate(self.note6),
                  Uncreate(s1), Uncreate(s2), Uncreate(s3), Uncreate(s4), Uncreate(s5),
                  Uncreate(line1), Uncreate(line2), Uncreate(line3))

        self.note1 = Tex(r'下面是c语言实现的无序查找表代码,查找表元素节点与链表节点创建代码:',
                         tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))
        self.code1 = Code('struct_node.c', language='c', font_size=20, line_spacing=0.5, insert_line_no=False, margin=0.1) \
            .next_to(self.note1, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.code1))
        self.note2 = Tex(r'查找表更新代码:',
                         tex_template=my_ctex(22), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF)
        self.note2.move_to([MED_SMALL_BUFF, self.note2.get_center()[1], 0], LEFT)
        self.play(Create(self.note2))
        self.code2 = Code('st_put.c', language='c', font_size=18, line_spacing=0.5, insert_line_no=False,
                          margin=0.1) \
            .next_to(self.code1, RIGHT, SMALL_BUFF)
        self.code2.move_to([self.code2.get_critical_point(LEFT)[0], self.code1.get_critical_point(UP)[1], 0], UP+LEFT)
        self.play(Create(self.code2))

        self.wait(2)

        self.play(Uncreate(self.note1), Uncreate(self.note2),
                  Uncreate(self.code1), Uncreate(self.code2))

        self.note1 = Tex(r'假设这样的场景,我们要统计一下冰箱里面不同水果的数目,建立一张水果表.',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))

        self.note2 = Tex(r'建立表,苹果2个,香蕉3个,梨5个,桃3个,橙子2个,柠檬2个.',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note1, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note2))

        statusRect = RoundedRectangle(0.1, width=1, height=0.5).to_edge(RIGHT)
        statusRect.move_to([statusRect.get_center()[0], -1.5, 0])
        self.play(Create(statusRect))

        st = SearchTable(self, statusRect)

        st.put('apple', 2)
        st.put('banana', 3)
        st.put('pear', 5)
        st.put('peach', 3)
        st.put('orange', 2)
        st.put('lemon', 2)

        self.note3 = Tex(r'这时,我们发现香蕉的个数数错了,应该是4个.',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note2, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note3))
        st.put('banana', 4)

        self.note4 = Tex(r'当我们需要从表中查看苹果的个数时...',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.note3, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note4))
        st.get('apple')

        self.wait(1)
        self.play(Uncreate(self.note1), Uncreate(self.note2), Uncreate(self.note3), Uncreate(self.note4),
                  *st.clear(), Uncreate(statusRect))

        self.note1 = Tex(r'下面考虑复杂一点点的情况,假设我们要统计一篇文章中单词的个数,那么,每个单词读入以后都会对查找表做一次修改,这种情况下,'
                         r'访问次数将会取决于文章的单词总数以及不同单词的个数,比如下面的例子:',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))

        words = 'I am a dog I am not a dog'.split(' ')
        wordObjs = []
        animations = []
        for i, word in enumerate(words):
            if i == 0:
                obj = Tex(word, tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
                    .next_to(self.note1, DOWN, MED_SMALL_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
                wordObjs.append(obj)
            else:
                obj = Tex(word, tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
                    .next_to(wordObjs[-1], RIGHT, MED_SMALL_BUFF)
                wordObjs.append(obj)
            self.play(Create(obj, run_time=0.1))
            animations.append(Uncreate(obj))

        statusRect = RoundedRectangle(0.1, width=1, height=0.5).to_edge(RIGHT)
        statusRect.move_to([statusRect.get_center()[0], -1.5, 0])
        self.play(Create(statusRect))

        st = SearchTable(self, statusRect, run_time=0.5)

        for word, wordobj in zip(words, wordObjs):
            self.play(wordobj.animate(run_time=0.5).set_color(RED))
            count = st.get(word)
            if count:
                st.put(word, count+1)
            else:
                st.put(word, 1)
            self.play(wordobj.animate(run_time=0.5).set_color(WHITE))

        self.wait(1)

        self.play(Uncreate(self.note1), Uncreate(statusRect), *animations, *st.clear())

        self.note1 = Tex(r'显然可见,对于大文本,无序查找表不是什么好主意,下面我们统计了<双城记>获得词频表的比较次数,将第i个词更新词频表的比较次数以及'
                         r'前i次的平均比较次数绘制成曲线如下,其中,蓝色为每个词的比较次数,红色为前i次的平均比较次数.',
                         tex_template=my_ctex(44), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))

        data = np.load('assets/results.npy', allow_pickle=True)
        axes = Axes([0, int(np.max(data, 0)[0]), int(np.max(data, 0)[0]) // 2],
                    [0, int(max(np.max(data, 0)[1], np.max(data, 0)[2])),
                     int(max(np.max(data, 0)[1], np.max(data, 0)[2])) // 2],
                    y_length=config.frame_height - 3.5, axis_config={'include_numbers': True}) \
            .next_to(self.note1, DOWN, MED_SMALL_BUFF)
        self.play(Create(axes))
        group = VMobject()
        for i, row in enumerate(data):
            dot1 = Dot(axes.coords_to_point(row[0], row[1]), color=BLUE, radius=0.01)
            dot2 = Dot(axes.coords_to_point(row[0], row[2]), color=RED, radius=0.01)
            group.add(dot1, dot2)
        self.add(group)

        self.wait(3)
        self.play(Uncreate(self.title), Uncreate(self.note1), Uncreate(axes))
        self.remove(group)
        self.title = Tex('参考文献',
                         tex_template=my_ctex(), font_size=48).to_edge(UP, MED_SMALL_BUFF)
        self.play(Create(self.title))
        self.note1 = Tex(r'[1]算法:第4版/(美)塞奇威克,(美)韦恩 著;谢路云 译.-- 北京:人民邮电出版社,2012.10',
                         tex_template=my_ctex(45), tex_environment='flushleft', font_size=28) \
            .next_to(self.title, DOWN, MED_LARGE_BUFF).to_edge(LEFT, MED_SMALL_BUFF)
        self.play(Create(self.note1))
