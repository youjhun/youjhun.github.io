"""MIT HST.582J 단시간 푸리에 변환 문서의 그림.

말소리를 흉내 낸 합성 신호를 쓴다. 기본 주파수가 100 Hz에서 140 Hz로 오르는 펄스 열을
500, 1500, 2500 Hz의 공진기 세 개에 통과시켰다. 표본화 주파수는 10 kHz다.
신호와 공진기 값은 예로 정한 것이고, 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, stft, get_window

from style import BLUE, ORANGE, save, setup

setup()
ARTICLE = "stft-spectrogram"
FS = 10_000
T = 0.6
n = np.arange(int(T * FS))
f0 = 100 + 40 * n / len(n)
phase = np.cumsum(f0 / FS)
x = np.zeros(len(n))
x[np.nonzero(np.diff(np.floor(phase)) > 0)[0] + 1] = 1.0
for fc, bw in [(500, 80), (1500, 120), (2500, 160)]:
    r = np.exp(-np.pi * bw / FS)
    a = [1, -2 * r * np.cos(2 * np.pi * fc / FS), r * r]
    x = lfilter([1 - r], a, x)
x = x / np.max(np.abs(x))

# 그림 1: 한 시각에서 10 ms와 40 ms 해밍 창으로 본 스펙트럼
n0 = int(0.15 * FS)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
for ax, ms, c in zip(axes, (10, 40), (ORANGE, BLUE)):
    L = int(ms * FS / 1000)
    w = get_window("hamming", L)
    seg = x[n0 - L // 2 : n0 - L // 2 + L] * w
    X = np.fft.rfft(seg, 4096)
    f = np.fft.rfftfreq(4096, 1 / FS)
    ax.plot(f, 20 * np.log10(np.abs(X) / np.max(np.abs(X)) + 1e-9), color=c, lw=1.4)
    ax.set_xlim(0, 3000)
    ax.set_ylim(-60, 3)
    ax.set_xlabel("주파수 (Hz)")
    ax.set_title(f"{ms} ms 해밍 창", loc="left")
axes[0].set_ylabel("크기 (dB)")
fig.tight_layout()
save(fig, ARTICLE, "window-length-spectra.png")

# 그림 2: 광대역·협대역 스펙트로그램
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
for ax, ms in zip(axes, (5, 40)):
    L = int(ms * FS / 1000)
    f, t, Z = stft(x, fs=FS, window="hamming", nperseg=L, noverlap=L - max(1, L // 8), nfft=2048, boundary=None)
    S = 20 * np.log10(np.abs(Z) + 1e-6)
    S -= S.max()
    ax.pcolormesh(t, f, S, vmin=-40, vmax=0, cmap="Greys", shading="auto")
    ax.set_ylim(0, 3000)
    ax.set_xlabel("시간 (s)")
    ax.set_title(f"{ms} ms 해밍 창", loc="left")
    ax.grid(False)
axes[0].set_ylabel("주파수 (Hz)")
fig.tight_layout()
save(fig, ARTICLE, "spectrograms.png")

for ms in (5, 10, 40):
    N = ms * FS // 1000
    print(ms, "ms: N =", N, " 2/N in Hz =", 2 / N * FS, " hop N/4 =", N // 4)
