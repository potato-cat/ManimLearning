from manim import *
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import get_window
from FreqTable import FreqTable, Gains
from tempfile import mktemp

filename = 'tone.wav'

base = 'C'
speed = 112
music1 = '6, 3 3 3_. 4__ & ( 3 - 3_ ) 3_ 4_ 5_ & 6. 6_ 5 5 & 3 - - - ||' \
         '6, 2 2 2_. 3__ & 2 - 3 - & 5_. 3__ 5 - 7,_. 1__ & ( 6, - - - ) ||' \
         '6, 6, 1 3 & 6_. 5__ ( 6 - 6_. ) 5__ 6_. 5__ 6 - 5_. 5__ ( 3 - - - ) ||' \
         '3 2 6 5 3_. 2__ ( 3 - - 3 ) 2 6 4 3_. 2__ 3 5 7,_. 1__ 6, - - -'

music2 = '0 0 0 0 & 0 0 0 0 & 0 0 0 0 & 0 0 0 0 || ' \
         '2,,|2, 2,|4,, 0 0 & 2,,|2,,, 2,|4,, 0 0 & 3,,|3,,, 2,|5,, 0 0 & 2,,|2,,, 2,|4,, 0 1,|4,, || ' \
         '2,,|2,,, 2,|6,, 2,|6,,|4,, 2|6,,|2,, & 4,,|4,,, 2,|6,, 4,,|4,,, 1,|6,, & 4,,|4,,, 2,|6,, 4,,|4,,, ' \
         '1,|6,, & 6,,|6,,, 3,|1, 6,|6,, 3,|7,, ||' \
         '6,,|6,,, 2,|4,, 6,,|6,,, 2,|5,, & 3,,|3,,, 2,|6,, 3,,|3,,, 1,|5,, & 3,,|3,,, 4,|6,, 0 2,|6,, & ' \
         '3,,|3,,, 3,|7,, 0 2,|7,, ||' \
         '6,,|3,, - - -'

INTERVAL = 0.2
N = 8192
Fs = 44100
MULTIP1 = 0.9
MULTIP2 = 1.1


class Music2Scene(Scene):
    def construct(self):
        self.title = Tex('太阳照常升起',
                         tex_template=TexTemplateLibrary.ctex, font_size=48).to_edge(UP)
        self.play(Create(self.title))
        self.cLine1 = None
        self.cLine2 = None
        self.currentPhase = 0
        self.toneTex = None
        self.lastFunctionTex = None
        handling = False
        handle = []
        self.interval = 60 / speed
        self.lastFreq = None
        self.lastTone1 = None
        self.lastTone2 = None
        self.currentTime = 0
        self.currentAnimations = []
        self.animationTime = 0

        # 处理文本
        lines1 = music1.split('||')
        words1 = [section for line in lines1 for section in line.split()]

        lines2 = music2.split('||')
        words2 = [section for line in lines2 for section in line.split()]

        # text = ''
        # for tone in music1.split():
        #     if tone == 'SECTION':
        #         text += r'\\'
        #         continue
        #     for s in tone:
        #         text += r'\%s' % s if s == '_' or s == '.' else s
        #     text += ' \quad '
        # note = Tex('简谱',
        #            tex_template=TexTemplateLibrary.ctex, font_size=28) \
        #     .next_to(self.title, DOWN)
        # note1 = Tex('1=F', font_size=24).next_to(note, RIGHT, LARGE_BUFF, aligned_edge=DOWN)
        # score = Tex(r'\begin{spacing}{1.5}%s\end{spacing}' % text,
        #             tex_environment='flushleft',
        #             font_size=24) \
        #     .next_to(note, DOWN, MED_LARGE_BUFF)
        # self.play(Create(score), Create(note), Create(note1))
        # self.wait(1)
        # self.play(Uncreate(score), Uncreate(note), Uncreate(note1))

        self.axes = Axes(x_range=[0, 1 / 20 + 1 / 200, 2 / 200],
                         y_range=[-0.3, 0.3, 0.3],
                         tips=True,
                         y_length=2.5,
                         axis_config={"include_numbers": False,
                                      "include_ticks": False}).next_to(self.title, DOWN, 1)
        self.axes2 = Axes(x_range=[0, 1 / 20 + 1 / 200, 2 / 200],
                          y_range=[-1.5, 1.8, 0.5],
                          tips=True,
                          y_length=2.5,
                          axis_config={"include_numbers": False,
                                       'include_ticks': False}) \
            .next_to(self.axes, DOWN)
        self.note1 = Tex('一声部',
                         tex_template=TexTemplateLibrary.ctex, font_size=24).next_to(self.axes, LEFT, SMALL_BUFF)
        self.note2 = Tex('二声部',
                         tex_template=TexTemplateLibrary.ctex, font_size=24).next_to(self.axes2, LEFT, SMALL_BUFF)
        self.play(Create(self.axes), Create(self.axes2), Create(self.note1), Create(self.note2))
        self.handling1 = False
        self.handling2 = False
        self.continuousTones1 = []
        self.continuousTones2 = []
        self.wav1 = np.array([])
        self.wav2 = np.array([])
        i = 0
        j = 0
        while i < len(words1) or j < len(words2):
            tone1 = None
            tone2 = None
            if i < len(words1):
                tone1 = words1[i]
            if j < len(words2):
                tone2 = words2[j]
            logger.info('tone1:%s\ttone2:%s' % (tone1, tone2))
            if tone1:
                self.handleTone1(tone1)
            if tone2:
                self.handleTone2(tone2)
            self.playWav()
            i += 1
            j += 1

        self.wait(2)

    def playWav(self):
        logger.info('len1: %d\tlen2:%d' % (len(self.wav1), len(self.wav2)))
        if len(self.wav1) > len(self.wav2):
            time = len(self.wav2) / Fs
            wav = MULTIP1 * self.wav1[0:len(self.wav2)] + MULTIP2 * self.wav2
            self.wav1 = self.wav1[len(self.wav2): len(self.wav1)]
            self.wav2 = np.array([])
            write(filename, Fs, self.toPCM(wav))
            self.add_sound(filename)
        else:
            time = len(self.wav1) / Fs
            wav = MULTIP2 * self.wav2[0:len(self.wav1)] + MULTIP1 * self.wav1
            self.wav2 = self.wav2[len(self.wav1): len(self.wav2)]
            self.wav1 = np.array([])
            write(filename, Fs, self.toPCM(wav))
            self.add_sound(filename)
        if len(self.currentAnimations):
            for animation in self.currentAnimations:
                animation.set_run_time(min(animation.run_time, time))
            self.play(*self.currentAnimations)
            self.currentAnimations = []
            self.wait(time - min(animation.run_time, time))
        else:
            self.wait(time)

    def createToneTex(self, tone, font_size=28):
        if tone[-1] == ',':
            tex = Tex('音符：$\mathop{%s}\limits_{\cdot}$' % tone[1],
                      tex_template=TexTemplateLibrary.ctex, font_size=font_size)
        elif tone[-1] == '\'':
            tex = Tex('音符：$\dot{%s}$' % tone[1],
                      tex_template=TexTemplateLibrary.ctex, font_size=font_size)
        else:
            tex = Tex('音符：$%s$' % tone[0],
                      tex_template=TexTemplateLibrary.ctex, font_size=font_size)
        return tex

    def handleContinuous1(self):
        tones = []
        times = []
        for tone in self.continuousTones1:
            if tone == '-':
                tone = self.lastTone1
                trueTone, time = self.convertTone(tone)
            elif tone == '0':
                trueTone = None
                time = self.interval
                self.lastTone1 = tone
            else:
                trueTone, time = self.convertTone(tone)
                self.lastTone1 = tone
            tones.append(trueTone)
            times.append(time)
        logger.info('连音音符：%s, 连音时间: %s' % (str(tones), str(times)))
        if len(set(tones)) == 1:
            wav = self.playTone(tones[0], base, sum(times))
            return wav
        else:
            # self.playFreqContinuous(freqs, times)
            wavs = []
            for tone, time in zip(tones, times):
                wavs.append(self.playTone(tone, base, time))
            return np.concatenate(wavs)

    def handleContinuous2(self):
        tones = []
        times = []
        for tone in self.continuousTones2:
            if tone == '-':
                tone = self.lastTone2
                trueTone, time = self.convertTone(tone)
            elif tone == '0':
                trueTone = None
                time = self.interval
                self.lastTone2 = tone
            else:
                trueTone, time = self.convertTone(tone)
                self.lastTone2 = tone
            tones.append(trueTone)
            times.append(time)
        logger.info('连音音符：%s, 连音时间: %s' % (str(tones), str(times)))
        if len(set(tones)) == 1:
            wav = self.playTone(tones[0], base, sum(times))
            return wav
        else:
            # self.playFreqContinuous(freqs, times)
            wavs = []
            for tone, time in zip(tones, times):
                wavs.append(self.playTone(tone, base, time))
            return np.concatenate(wavs)

    def handleTone1(self, tone: str):
        if tone == '&':
            return
        if tone == '(':
            self.handling1 = True
            return
        elif tone == ')':
            self.handling1 = False
            wav = self.handleContinuous1()
            wav = wav / np.max(wav) * 0.5
            self.continuousTones1 = []
            self.wav1 = np.concatenate([self.wav1, wav])
            return
        if self.handling1:
            self.continuousTones1.append(tone)
            return

        if tone == '-':
            tone = self.lastTone1

        if tone == '0':
            self.lastTone1 = tone
            wav = self.playTone(None, time=self.interval)
            self.wav1 = np.concatenate([self.wav1, wav])
            return
        if '|' in tone:
            tones = tone.split('|')
            wavs = []
            trueTones = []
            for t in tones:
                trueTone, time = self.convertTone(t)
                wavs.append(self.playTone(trueTone, base, time))
                trueTones.append(trueTone)
            x, f = self.sinCurve(trueTones)
            wav = np.sum(wavs, 0)
            wav = wav / np.max(wav) * 0.5
            self.wav1 = np.concatenate([self.wav1, wav])
            cLine = self.axes.plot(f, x)
            if self.cLine1 == None:
                self.cLine1 = cLine
                self.currentAnimations.append(Create(self.cLine1, run_time=INTERVAL))
            else:
                self.currentAnimations.append(ReplacementTransform(self.cLine1, cLine, run_time=INTERVAL))
                self.cLine1 = cLine
            self.lastTone1 = tone
            return
        trueTone, time = self.convertTone(tone)
        wav = self.playTone(trueTone, base, time)
        wav = wav / np.max(wav) * 0.5
        self.wav1 = np.concatenate([self.wav1, wav])
        x, f = self.sinCurve(trueTone)
        cLine = self.axes.plot(f, x, color=BLUE)
        if self.cLine1 == None:
            self.cLine1 = cLine
            self.currentAnimations.append(Create(self.cLine1, run_time=INTERVAL))
        else:
            self.currentAnimations.append(ReplacementTransform(self.cLine1, cLine, run_time=INTERVAL))
            self.cLine1 = cLine
        self.lastTone1 = tone
        return

    def handleTone2(self, tone: str):
        if tone == '&':
            return
        if tone == '(':
            self.handling2 = True
            return
        elif tone == ')':
            self.handling2 = False
            wav = self.handleContinuous2()
            wav = wav / np.max(wav) * 0.5
            self.continuousTones2 = []
            self.wav2 = np.concatenate([self.wav2, wav])
            return
        if self.handling2:
            self.continuousTones2.append(tone)
            return

        if tone == '-':
            tone = self.lastTone2

        if tone == '0':
            self.lastTone2 = tone
            wav = self.playTone(None, time=self.interval)
            self.wav2 = np.concatenate([self.wav2, wav])
            return
        if '|' in tone:
            tones = tone.split('|')
            wavs = []
            trueTones = []
            for t in tones:
                trueTone, time = self.convertTone(t)
                wavs.append(self.playTone(trueTone, base, time))
                trueTones.append(trueTone)
            x, f = self.sinCurve(trueTones)
            wav = np.sum(wavs, 0)
            wav = wav / np.max(wav) * 0.5
            self.wav2 = np.concatenate([self.wav2, wav])
            cLine = self.axes2.plot(f, x, color=BLUE)
            if self.cLine2 == None:
                self.cLine2 = cLine
                self.currentAnimations.append(Create(self.cLine2, run_time=INTERVAL))
            else:
                self.currentAnimations.append(ReplacementTransform(self.cLine2, cLine, run_time=INTERVAL))
                self.cLine2 = cLine
            self.lastTone2 = tone
            return
        trueTone, time = self.convertTone(tone)
        wav = self.playTone(trueTone, base, time)
        wav = wav / np.max(wav) * 0.5
        self.wav2 = np.concatenate([self.wav2, wav])
        x, f = self.sinCurve(trueTone)
        cLine = self.axes2.plot(f, x, color=BLUE)
        if self.cLine2 == None:
            self.cLine2 = cLine
            self.currentAnimations.append(Create(self.cLine2, run_time=INTERVAL))
        else:
            self.currentAnimations.append(ReplacementTransform(self.cLine2, cLine, run_time=INTERVAL))
            self.cLine2 = cLine
        self.lastTone2 = tone
        return

    def convertTone(self, tone):
        multi = 1
        addition = 0
        i = len(tone) - 1
        while i >= 0:
            if tone[i] == '.':
                addition += 0.5
                i -= 1
                continue
            if tone[i] == '_':
                multi *= 0.5
                i -= 1
                continue
            if tone[i].isdecimal() or tone[i] == '\'' or tone[i] == ',' \
                    or tone[i] == '‘' or tone[i] == '，':
                trueTone = tone[0:i + 1]
                break
            i -= 1
        time = self.interval * multi * (1 + addition)
        return trueTone, time

    def playTone(self, tone, base='C', time=1., interval=0.):
        if tone == None:
            return np.zeros(int((time - interval) * Fs))
        index = self.toneIndex(tone, base)
        freq = FreqTable[index]
        y = self.sinWave(Fs, tone, time - interval)
        # split = len(y) // 2
        split = 440
        # gain = np.concatenate([1 - np.exp(-np.arange(0, split) / split * 10),
        #                        np.ones(len(y) - 2 * split),
        #                        np.flip(1 - np.exp(-np.arange(0, split) / split * 10))])
        # gain = np.concatenate([np.arange(0, split) / split,
        #                        np.ones(len(y) - 2 * split),
        #                        np.flip(np.arange(0, split) / split)])
        gain = np.concatenate(
            [1 - np.exp(-np.arange(split)), np.exp(-np.arange(len(y) - split) / (len(y) - split) * 2)])
        yw = y * gain
        return yw

    def sinCurve(self, tones):
        if type(tones) == str:
            tones = [tones]
        indexes = [self.toneIndex(tone, base) for tone in tones]

        freqs = [FreqTable[index] for index in indexes]
        x = [0, 1 / 20, 1 / (10 * max(freqs))]
        gains = []
        for index in indexes:
            if index in Gains:
                gains.append(Gains[index])
            elif index < 36:
                gains.append([0.07144, 0.05695, 0.08564, 0.02094, 0.0231, 0.06566, 0.03254, 0.001663, 0.02307, 0.03251,
                              0.01642,
                              0.003389, 0.01135, 0.01686, 0.007084, 0.001784, 0.00516, 0.005182, 0.002537, 0.004612,
                              0.003989,
                              0.004442])
            else:
                gains.append([0.02913, 0.001935, 0.0003091])
        return x, lambda x: sum([gains[i][j] * np.sin(2 * PI * (i + 1) * freqs[i] * x)
                                 for i in range(len(freqs)) for j in range(len(gains[i]))])

    def sinWave(self, fs, tone, time):
        index = self.toneIndex(tone, base)
        freq = FreqTable[index]
        if index in Gains:
            gains = Gains[index]
        elif index < 36:
            gains = [0.07144, 0.05695, 0.08564, 0.02094, 0.0231, 0.06566, 0.03254, 0.001663, 0.02307, 0.03251, 0.01642,
                     0.003389, 0.01135, 0.01686, 0.007084, 0.001784, 0.00516, 0.005182, 0.002537, 0.004612, 0.003989,
                     0.004442]
        else:
            gains = [0.02913, 0.001935, 0.0003091]
        x = np.arange(0, time, 1 / fs)
        y = np.zeros(len(x))
        for i in range(0, len(gains)):
            y += gains[i] * np.sin(2 * PI * (i + 1) * freq * x)
        return y

    def singleWave(self, fs, freq, time):
        x = np.arange(0, time, 1 / fs)
        y = np.sin(2 * PI * freq * x)
        return y

    def getPhase(self, phase):
        while phase > 2 * PI:
            phase -= 2 * PI
        return phase

    def toPCM(self, y):
        return np.int32(2147483647 * y)

    def toneIndex(self, tone: str, base: str):
        if base == 'F':
            base = 77
        elif base == 'Cb':
            base = 60
        else:
            base = 72
        tone_num = int(tone[0])
        addition = 0
        for i in range(1, len(tone)):
            if tone[i] == '\'' or tone[i] == '’':
                addition += 12
            elif tone[i] == ',' or tone[i] == '，':
                addition -= 12
        if tone_num <= 3:
            tone_num = base + 2 * (tone_num - 1)
        elif tone_num == 4:
            tone_num = base + 5
        elif 4 < tone_num <= 7:
            tone_num = base + 5 + 2 * (tone_num - 4)
        tone_num = tone_num + addition
        return tone_num
