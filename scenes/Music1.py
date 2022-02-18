from manim import *
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import get_window
from FreqTable import FreqTable
from tempfile import mktemp

filename = 'tone.wav'

base = 'F'
speed = 112
music = ['L6', '3', '3', '3_.', '4__', '(', '3', '-', '3_', ')', '3_', '4_', '5_',
         '6.', '6_', '5', '5', '3', '-', '-', '-', 'SECTION',
         'L6', '2', '2', '2_.', '3__', '2', '-', '3', '-', '5_.', '3__', '5', '-', 'L7_.',
         '1__', '(', 'L6', '-', '-', '-', ')', 'SECTION',
         'L6', 'L6', '1', '3', '6_.', '5__', '(', '6', '-', '6_.', ')', '5__', '6_.', '5__',
         '6', '-', '5_.', '5__', '(', '3', '-', '-', '-', ')', 'SECTION',
         '3', '2', '6', '5', '3_.', '2__', '(', '3', '-', '-', '3', ')', '2', '6', '4',
         '3_.', '2__', '3', '5', 'L7_.', '1__',
         'L6', '-', '-', '-']
INTERVAL = 0.2
N = 8192
Fs = 44100


class Music1Scene(Scene):
    def construct(self):
        self.title = Tex('太阳照常升起',
                         tex_template=TexTemplateLibrary.ctex, font_size=48).to_edge(UP)
        self.play(Create(self.title))
        self.cLine = None
        self.cFFTLine = None
        self.currentPhase = 0
        self.toneTex = None
        self.lastFunctionTex = None
        handling = False
        handle = []
        self.interval = 60 / speed
        self.lastFreq = None
        self.lastTone = None

        table = Tex(r'''\begin{table}[h!]
                                  \begin{center}
                                    \caption{音符频率}
                                    \begin{tabular}{l|l|l|l|l|l}
                                      \textbf{音符} & \textbf{频率/Hz} & \textbf{音符} & \textbf{频率/Hz} &\textbf{音符} & \textbf{频率/Hz} \\
                                      \hline
                                       $\mathop{1}\limits_{\cdot}$ & 262 & $1$ & 523 & $\dot{1}$ & 1046 \\
                                       $\mathop{2}\limits_{\cdot}$ & 294 & $2$ & 587 & $\dot{2}$ & 1175 \\
                                       $\mathop{3}\limits_{\cdot}$ & 330 & $3$ & 659 & $\dot{3}$ & 1318 \\
                                       $\mathop{4}\limits_{\cdot}$ & 349 & $4$ & 698 & $\dot{4}$ & 1397 \\
                                       $\mathop{5}\limits_{\cdot}$ & 392 & $5$ & 784 & $\dot{5}$ & 1568 \\
                                       $\mathop{6}\limits_{\cdot}$ & 440 & $6$ & 880 & $\dot{6}$ & 1760 \\
                                       $\mathop{7}\limits_{\cdot}$ & 494 & $7$ & 988 & $\dot{7  }$ & 1976 \\
                                    \end{tabular}
                                  \end{center}
                                \end{table}
                                ''',
                    tex_template=TexTemplateLibrary.ctex, font_size=30).next_to(self.title, DOWN, MED_LARGE_BUFF)
        self.play(Create(table))
        self.wait(2)
        self.play(Uncreate(table))

        self.axes = Axes(x_range=[0, 1 / 262, 2 / 2620],
                         y_range=[-1.5, 1.8, 0.5],
                         tips=True,
                         y_length=2.5,
                         axis_config={"include_numbers": False,
                                      "include_ticks": False}).next_to(self.title, DOWN, 1)
        self.axes2 = Axes(x_range=[0, 3000, 500],
                          y_range=[0, 1, 0.5],
                          tips=False,
                          y_length=2.5,
                          axis_config={"include_numbers": True,
                                       'tick_size': 0.05}) \
            .next_to(self.axes, DOWN) \
            .shift([-0.1, 0, 0])
        self.play(Create(self.axes), Create(self.axes2))

        for tone in ['1', '2', '3', '4', '5', '6', '7']:
            freq, time = self.handleTone(tone, 'C')
            functionTex = Tex(r'$y = \sin \left( {2\pi \times %dt} \right)$' % int(freq),
                              tex_template=TexTemplateLibrary.ctex, font_size=28) \
                .next_to(self.title, DOWN)
            if self.lastFunctionTex is None:
                self.lastFunctionTex = functionTex
                self.play(Create(functionTex))
            else:
                self.play(ReplacementTransform(self.lastFunctionTex, functionTex))
                self.lastFunctionTex = functionTex
            self.playSingleFreq(freq, time, 0)
        self.play(Uncreate(self.lastFunctionTex),
                  Uncreate(self.axes), Uncreate(self.axes2),
                  Uncreate(self.toneTex), Uncreate(self.cLine),
                  Uncreate(self.cFFTLine))
        self.toneTex = None
        self.cLine = None
        self.cFFTLine = None
        self.lastFreq = None
        self.lastTone = None

        note = Tex(r'加点衰减，$y = \rm{e}^{-ax}\sin\left({2\pi \times 523x}\right)$',
                   tex_template=TexTemplateLibrary.ctex,
                   tex_environment='flushleft',
                   font_size=24).next_to(self.title, DOWN).to_edge(LEFT)
        self.play(Create(note))
        self.axes = Axes(x_range=[0, 0.5, 0.1],
                         y_range=[-1.5, 1.8, 0.5],
                         tips=True,
                         y_length=2.5,
                         axis_config={"include_numbers": False,
                                      "include_ticks": False}).next_to(self.title, DOWN, 1)
        self.axes2 = Axes(x_range=[0, 3, 1],
                          y_range=[0, 1, 0.5],
                          tips=True,
                          y_length=2.5,
                          axis_config={"include_numbers": False,
                                       "include_ticks": False,
                                       'tick_size': 0.05}) \
            .next_to(self.axes, DOWN) \
            .shift([-0.1, 0, 0])
        self.play(Create(self.axes), Create(self.axes2))

        wavLine = self.axes.plot(lambda x: np.sin(2 * PI * 523 * x), [0, 0.5, 1 / 5230], stroke_color=BLUE)
        exLine = self.axes2.plot(lambda x: np.exp(-x), [0, 3, 0.1], stroke_color=BLUE)
        self.play(Create(wavLine), Create(exLine))
        wavExLine = self.axes.plot(lambda x: np.exp(-4 * x) * np.sin(2 * PI * 523 * x),
                                   [0, 0.5, 1 / 5230], stroke_color=RED)
        wav = self.singleWave(Fs, 523, 1)
        attenation = np.exp(-np.arange(0, len(wav)) / len(wav) * 3)
        write(filename, Fs, self.toPCM(wav * attenation))
        self.add_sound(filename)
        self.play(Create(wavExLine, run_time=1))
        self.wait(1)
        self.play(Uncreate(wavExLine),
                  Uncreate(wavLine),
                  Uncreate(exLine),
                  Uncreate(self.axes),
                  Uncreate(self.axes2),
                  Uncreate(note))

        note = Tex(r'叠加谐波，$y = \sum\limits_{i = 1}^N {\sin \left( {2\pi \times 523ix} \right)}$',
                   tex_template=TexTemplateLibrary.ctex,
                   tex_environment='flushleft',
                   font_size=24).next_to(self.title, DOWN).to_edge(LEFT)
        self.play(Create(note))

        self.axes = Axes(x_range=[0, 1 / 262, 10 / 262],
                         y_range=[-0.5, 0.8, 0.5],
                         tips=True,
                         y_length=2.5,
                         axis_config={"include_numbers": False,
                                      "include_ticks": False}).next_to(self.title, DOWN, 1)
        self.axes2 = Axes(x_range=[0, 1 / 262, 10 / 262],
                          y_range=[-0.5, 0.8, 0.5],
                          tips=True,
                          y_length=2.5,
                          axis_config={"include_numbers": False,
                                       "include_ticks": False,
                                       'tick_size': 0.05}) \
            .next_to(self.axes, DOWN) \
            .shift([-0.1, 0, 0])
        self.play(Create(self.axes), Create(self.axes2))
        lines = []
        colors = [BLUE, GREEN, YELLOW, RED, PINK]
        gains = [0.368847, 0.237165, 0.209451, 0.078583, 0.055452, 0.081702, 0.046401, 0.017056,
                 0.025370, 0.005480, 0.006849, 0.006203, 0.009581, 0.002050, 0.004867, 0.001362,
                 0.001362, 0.001362]
        for i in range(1, 6):
            line = self.axes.plot(lambda x: gains[i - 1] * np.sin(2 * PI * 523 * i * x), [0, 1 / 262, 1 / 2620],
                                  stroke_color=colors[i - 1])
            lines.append(line)
        self.play(*[Create(line) for line in lines])
        line = self.axes2.plot(lambda x: sum([gains[i - 1] * np.sin(2 * PI * 523 * i * x) for i in range(1, 6)]),
                               [0, 1 / 262, 1 / 2620],
                               stroke_color=BLUE)
        wav = self.sinWave(Fs, 523, 1)
        attenation = np.exp(-np.arange(0, len(wav)) / len(wav) * 3)
        write(filename, Fs, self.toPCM(wav * attenation))
        self.add_sound(filename)
        self.play(Create(line, run_time=1))
        self.wait(1)
        self.play(Uncreate(line),
                  *[Uncreate(line) for line in lines],
                  Uncreate(self.axes),
                  Uncreate(self.axes2),
                  Uncreate(note))

        self.axes = Axes(x_range=[0, 1 / 262, 2 / 2620],
                         y_range=[-1.5, 1.8, 0.5],
                         tips=True,
                         y_length=2.5,
                         axis_config={"include_numbers": False,
                                      "include_ticks": False}).next_to(self.title, DOWN, 1)
        self.axes2 = Axes(x_range=[0, 3000, 500],
                          y_range=[0, 1, 0.5],
                          tips=False,
                          y_length=2.5,
                          axis_config={"include_numbers": True,
                                       'tick_size': 0.05}) \
            .next_to(self.axes, DOWN) \
            .shift([-0.1, 0, 0])
        self.play(Create(self.axes), Create(self.axes2))

        for tone in ['1', '2', '3', '4', '5', '6', '7']:
            freq, time = self.handleTone(tone, 'C')
            self.playFreq(freq, time, 0)

        self.play(Uncreate(self.axes), Uncreate(self.axes2),
                  Uncreate(self.toneTex), Uncreate(self.cLine),
                  Uncreate(self.cFFTLine))
        self.toneTex = None
        self.cLine = None
        self.cFFTLine = None
        self.lastFreq = None
        self.lastTone = None

        text = ''
        for tone in music:
            if tone == 'SECTION':
                text += r'\\'
                continue
            for s in tone:
                text += r'\%s' % s if s == '_' or s == '.' else s
            text += ' \quad '
        note = Tex('简谱',
                   tex_template=TexTemplateLibrary.ctex, font_size=28) \
            .next_to(self.title, DOWN)
        note1 = Tex('1=F', font_size=24).next_to(note, RIGHT, LARGE_BUFF, aligned_edge=DOWN)
        score = Tex(r'\begin{spacing}{1.5}%s\end{spacing}' % text,
                    tex_environment='flushleft',
                    font_size=24) \
            .next_to(note, DOWN, MED_LARGE_BUFF)
        self.play(Create(score), Create(note), Create(note1))
        self.wait(1)
        self.play(Uncreate(score), Uncreate(note), Uncreate(note1))

        self.axes = Axes(x_range=[0, 1 / 262, 2 / 2620],
                         y_range=[-1.5, 1.8, 0.5],
                         tips=True,
                         y_length=2.5,
                         axis_config={"include_numbers": False,
                                      "include_ticks": False}).next_to(self.title, DOWN, 1)
        self.axes2 = Axes(x_range=[0, 3000, 500],
                          y_range=[0, 1, 0.5],
                          tips=False,
                          y_length=2.5,
                          axis_config={"include_numbers": True,
                                       'tick_size': 0.05}) \
            .next_to(self.axes, DOWN) \
            .shift([-0.1, 0, 0])
        self.play(Create(self.axes), Create(self.axes2))

        for tone in music:
            if tone == 'SECTION':
                continue
            if tone == '(':
                handling = True
                handle = []
                continue
            elif tone == ')':
                handling = False
                logger.info('状态：连音, %s' % str(handle))
                self.handleContinuous(handle)
                continue
            if handling:
                handle.append(tone)
                continue
            logger.info('状态：单独音符')
            freq, time = self.handleTone(tone, base)
            self.playFreq(freq, time, 0)
        self.wait(2)

    def createToneTex(self, tone, font_size=28):
        if tone[0] == 'L':
            tex = Tex('音符：$\mathop{%s}\limits_{\cdot}$' % tone[1],
                      tex_template=TexTemplateLibrary.ctex, font_size=font_size)
        elif tone[0] == 'H':
            tex = Tex('音符：$\dot{%s}$' % tone[1],
                      tex_template=TexTemplateLibrary.ctex, font_size=font_size)
        else:
            tex = Tex('音符：$%s$' % tone[0],
                      tex_template=TexTemplateLibrary.ctex, font_size=font_size)
        return tex

    def handleContinuous(self, handle):
        freqs = []
        times = []
        for tone in handle:
            freq, time = self.handleTone(tone, base)
            freqs.append(freq)
            times.append(time)
        logger.info('连音音符：%s, 连音时间: %s' % (str(freqs), str(times)))
        if len(set(freqs)) == 1:
            self.playFreq(freqs[0], sum(times))
        else:
            # self.playFreqContinuous(freqs, times)
            for freq, time in zip(freqs, times):
                self.playFreq(freq, time)

    def handleTone(self, tone: str, base='C'):
        if tone == '-':
            tone = self.lastTone
            time = self.interval
            return self.toneFreq(tone, base), time
        if tone == '0':
            self.lastTone = tone
            return None, self.interval
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
            if tone[i].isdecimal():
                trueTone = tone[max(i - 1, 0):i + 1]
                break
            i -= 1
        self.lastTone = trueTone
        time = self.interval * multi * (1 + addition)
        return self.toneFreq(trueTone, base), time

    # def playFreqContinuous(self, freqs, times):
    #     wav = []
    #     phase = 0
    #     for freq, time in zip(freqs, times):
    #         y, phase = self.sinWave(Fs, freq, time, phase)
    #         wav.extend(self.toPCM(y))
    #         logger.info('y0:%f, y-1:%f' % (y[0], y[-1]))
    #     write('haha.wav', Fs, np.array(wav, dtype=np.int32))
    #     self.add_sound('haha.wav')
    #     for freq, time in zip(freqs, times):
    #         y = self.sinWave(Fs, freq, time)
    #         c = 3000 * N // Fs
    #         mag = (np.abs(np.fft.fft(y, N)) / N)[0:c]
    #         mag[1:c] = mag[1:c] * 2
    #         freqs = np.fft.fftfreq(N, 1 / Fs)[0:c]
    #         x, f = self.sinCurve(freq)
    #         line = self.axes.plot(f, x, stroke_color=BLUE)
    #         fftLine = self.axes2.plot_line_graph(freqs, mag, line_color=YELLOW, add_vertex_dots=False)
    #         if self.cLine is None:
    #             self.cLine = line
    #             self.cFFTLine = fftLine
    #             interval = min(INTERVAL, time)
    #             self.play(Create(line, run_time=interval),
    #                       Create(fftLine, run_time=interval))
    #             self.wait(time - interval)
    #         elif self.lastFreq != freq:
    #             interval = min(INTERVAL, time)
    #             self.play(ReplacementTransform(self.cLine, line, run_time=interval),
    #                       ReplacementTransform(self.cFFTLine, fftLine, run_time=interval))
    #             self.wait(time - interval)
    #             self.cLine = line
    #             self.cFFTLine = fftLine
    #         else:
    #             self.wait(time)
    #         self.lastFreq = freq

    def playSingleFreq(self, freq, time, interval=0):
        y = self.singleWave(Fs, freq, time - interval)
        split = len(y) // 2
        write(filename, Fs, self.toPCM(y))
        self.add_sound(filename)
        Nfft = min(N, len(y))
        c = 3000 * Nfft // Fs
        mag = (np.abs(np.fft.fft(y, Nfft)) / Nfft)[0:c]
        mag[1:c] = mag[1:c] * 2
        freqs = np.fft.fftfreq(Nfft, 1 / Fs)[0:c]

        line = self.axes.plot(lambda x: np.sin(2 * PI * freq * x), [0, 1 / 262, 1 / (10 * freq)],
                              stroke_color=BLUE)
        fftLine = self.axes2.plot_line_graph(freqs, mag, line_color=YELLOW, add_vertex_dots=False)

        tex = self.createToneTex(self.lastTone) \
            .next_to(self.title, DOWN) \
            .shift([3, 0, 0])
        if self.cLine is None:
            self.cLine = line
            self.cFFTLine = fftLine
            self.toneTex = tex
            interval = min(INTERVAL, time)
            self.play(Create(line, run_time=interval),
                      Create(fftLine, run_time=interval),
                      Create(self.toneTex, run_time=interval))
            self.wait(time - interval)
        elif self.lastFreq != freq:
            interval = min(INTERVAL, time)
            self.play(ReplacementTransform(self.cLine, line, run_time=interval),
                      ReplacementTransform(self.cFFTLine, fftLine, run_time=interval),
                      ReplacementTransform(self.toneTex, tex, run_time=interval))
            self.wait(time - interval)
            self.cLine = line
            self.cFFTLine = fftLine
            self.toneTex = tex
        else:
            self.wait(time)
        self.lastFreq = freq

    def playFreq(self, freq, time=1, interval=0):
        y = self.sinWave(Fs, freq, time - interval)
        split = len(y) // 2
        # gain = np.concatenate([1 - np.exp(-np.arange(0, split) / split * 10),
        #                        np.ones(len(y) - 2 * split),
        #                        np.flip(1 - np.exp(-np.arange(0, split) / split * 10))])
        # gain = np.concatenate([np.arange(0, split) / split,
        #                        np.ones(len(y) - 2 * split),
        #                        np.flip(np.arange(0, split) / split)])
        gain = np.exp(-np.arange(len(y)) / len(y) * 2)
        yw = y * gain
        write(filename, Fs, self.toPCM(yw))
        self.add_sound(filename)
        Nfft = min(N, len(y))
        c = 3000 * Nfft // Fs
        mag = (np.abs(np.fft.fft(y, Nfft)) / Nfft)[0:c]
        mag[1:c] = mag[1:c] * 2
        freqs = np.fft.fftfreq(Nfft, 1 / Fs)[0:c]

        x, f = self.sinCurve(freq)
        line = self.axes.plot(f, x, stroke_color=BLUE)
        fftLine = self.axes2.plot_line_graph(freqs, mag, line_color=YELLOW, add_vertex_dots=False)

        tex = self.createToneTex(self.lastTone) \
            .next_to(self.title, DOWN) \
            .shift([3, 0, 0])
        if self.cLine is None:
            self.cLine = line
            self.cFFTLine = fftLine
            self.toneTex = tex
            interval = min(INTERVAL, time)
            self.play(Create(line, run_time=interval),
                      Create(fftLine, run_time=interval),
                      Create(self.toneTex, run_time=interval))
            self.wait(time - interval)
        elif self.lastFreq != freq:
            interval = min(INTERVAL, time)
            self.play(ReplacementTransform(self.cLine, line, run_time=interval),
                      ReplacementTransform(self.cFFTLine, fftLine, run_time=interval),
                      ReplacementTransform(self.toneTex, tex, run_time=interval))
            self.wait(time - interval)
            self.cLine = line
            self.cFFTLine = fftLine
            self.toneTex = tex
        else:
            self.wait(time)
        self.lastFreq = freq

    def sinCurve(self, freq):
        x = [0, 1 / 262, 1 / (10 * freq)]
        gains = [0.368847, 0.237165, 0.209451, 0.078583, 0.055452, 0.081702, 0.046401, 0.017056,
                 0.025370, 0.005480, 0.006849, 0.006203, 0.009581, 0.002050, 0.004867, 0.001362,
                 0.001362, 0.001362]
        return x, lambda x: sum([gains[i] * np.sin(2 * PI * (i + 1) * freq * x)
                                 for i in range(len(gains))])

    def sinWave(self, fs, freq, time):
        gains = [0.368847, 0.237165, 0.209451, 0.078583, 0.055452, 0.081702, 0.046401, 0.017056,
                 0.025370, 0.005480, 0.006849, 0.006203, 0.009581, 0.002050, 0.004867, 0.001362,
                 0.001362, 0.001362]
        x = np.arange(0, time, 1 / fs)
        y = gains[0] * np.sin(2 * PI * freq * x)
        for i in range(1, 12):
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

    def toneFreq(self, tone: str, base: str):
        if base == 'F':
            base = 77
        elif base == 'Cb':
            base = 60
        else:
            base = 72
        if tone[0] == 'L':
            addition = -12
            tone = int(tone[1])
        elif tone[0] == 'H':
            addition = 12
            tone = int(tone[1])
        else:
            addition = 0
            tone = int(tone)
        if tone <= 3:
            tone = base + 2 * (tone - 1)
        elif tone == 4:
            tone = base + 5
        elif 4 < tone <= 7:
            tone = base + 5 + 2 * (tone - 4)
        tone = tone + addition
        return FreqTable[tone]
