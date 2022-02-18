from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import numpy as np
import os


def sinWave(fs, freq, time):
    gain = np.array([0.0237164945, 0.0368847482, 0.0209450962, 0.00785830407, 0.00554522229, 0.00817018904,
                     0.00464008404, 0.00170557676, 0.00253698843, 5.48026049E-4, 6.8485397E-4, 6.20292123E-4,
                     9.58092587E-4, 2.04974991E-4, 4.86672114E-4, 1.3618026E-4, 1.3618026E-4, 1.3618026E-4])
    # gain = np.array([0.0860459858, 0.0708480985, 0.0703349143, 0.0516976936, 0.0158022761, 0.0276664807,
    #                  0.00725582311, 0.005306814, 0.0021261949, 0.00130766863, 0.00105729076, 7.63008195E-4])
    gain = 20 * gain
    print(''.join(['%f,' % v for v in gain]))
    x = np.arange(0, time, 1 / fs)
    y = gain[0] * np.sin(2 * np.pi * freq * x)
    for i in range(1, 12):
        y += gain[i] * np.sin(2 * np.pi * (i + 1) * freq * x)
    gain = np.exp(-np.arange(len(y)) / len(y) * 2)
    return y * gain


Fs = 44100
data = sinWave(44100, 524 * 1, 0.4)
write('test.wav', 44100, np.concatenate([data, data, data, data]))
os.system('ffplay -autoexit test.wav')
# os.system('ffplay -autoexit 钢琴.wav')
# Fs, data = read('钢琴.wav')
# data = data / 32767
# # data = data[26000:80000, 1]
# data = data[104000:130000, 1]
# # N = (40000 - 23000)
# N = len(data)
# num = N * 7000 // Fs
# mag = np.abs(np.fft.fft(data))[0:num] / N
# mag[1:] = mag[1:] * 2
# freqs = np.fft.fftfreq(N, 1 / Fs)[0:num]
# np.savetxt('data.csv', np.array([freqs, mag]).T)
# plt.plot(freqs, mag)
# # plt.plot(data)
# plt.show()
#
# gain = np.array([0.15768, 0.023546, 0.092546, 0.013393, 0.010486,
#         0.00823, 0.003053, 0.002344, 0.003941])
# gain = 0.5/gain[0]*gain
# print(gain)

