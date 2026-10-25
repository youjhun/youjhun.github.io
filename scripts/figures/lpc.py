"""MIT HST.582J 선형 예측 문서의 그림.

합성 모음: 83 표본 간격(약 120.5 Hz) 펄스 열을 500, 1500, 2500, 3500 Hz 공진기에 통과시켰다.
표본화 주파수 10 kHz, 20 ms 해밍 창 구간을 자기상관법으로 분석한다. 레빈슨-더빈
재귀는 직접 구현했고 테플리츠 행렬 풀이와 같은 답을 내는지 확인한다. 값은 모두 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_toeplitz
from scipy.signal import lfilter

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()
ARTICLE = "linear-prediction"
FS = 10_000


def levinson(r, p):
    a = np.zeros(p + 1)
    e = r[0]
    errs = [e]
    for i in range(1, p + 1):
        k = (r[i] - np.dot(a[1:i], r[i - 1:0:-1])) / e
        new = a.copy()
        new[i] = k
        new[1:i] = a[1:i] - k * a[i - 1:0:-1]
        a = new
        e = (1 - k * k) * e
        errs.append(e)
    return a[1:], np.array(errs)


n = np.arange(int(0.2 * FS))
x = np.zeros(len(n))
x[:: FS // 120] = 1.0
for fc, bw in [(500, 60), (1500, 90), (2500, 120), (3500, 150)]:
    r_ = np.exp(-np.pi * bw / FS)
    x = lfilter([1 - r_], [1, -2 * r_ * np.cos(2 * np.pi * fc / FS), r_ * r_], x)
x = x / np.max(np.abs(x))
L = int(0.02 * FS)
s = x[1000:1000 + L] * np.hamming(L)
R = np.correlate(s, s, "full")[L - 1:]

NF = 4096
f = np.fft.rfftfreq(NF, 1 / FS)
S = np.abs(np.fft.rfft(s, NF)) ** 2
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
axes[0].plot(f, 10 * np.log10(S / S.max()), color=GRAY, lw=1, label="DFT 스펙트럼")
for p, c in [(4, ORANGE), (8, BLUE), (80, RED)]:
    a, errs = levinson(R, p)
    assert np.allclose(a, solve_toeplitz(R[:p], R[1:p + 1]))
    assert np.isclose(errs[-1], R[0] - a @ R[1:p + 1])
    A = np.fft.rfft(np.concatenate(([1.0], -a)), NF)
    H = errs[-1] / np.abs(A) ** 2
    axes[0].plot(f, 10 * np.log10(H / S.max()), color=c, lw=1.6, label=f"$p = {p}$")
axes[0].set_xlim(0, 5000)
axes[0].set_ylim(-70, 8)
axes[0].set_xlabel("주파수 (Hz)")
axes[0].set_ylabel("크기 (dB)")
axes[0].set_title("DFT 스펙트럼과 선형 예측 스펙트럼", loc="left")
axes[0].legend(fontsize=9, loc="lower left", ncol=2)

P = 30
_, errs = levinson(R, P)
pp = np.arange(P + 1)
aic = np.log(errs / errs[0]) + 2 * pp / L
axes[1].plot(pp, aic, "o-", color=TEAL, ms=3.5)
axes[1].axvline(int(np.argmin(aic)), color=GRAY, ls="--", lw=1)
axes[1].set_xlabel("모형 차수 $p$")
axes[1].set_ylabel("AIC")
axes[1].set_title("차수에 따른 AIC", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "lpc-spectra-order.png")
print("AIC min at p =", int(np.argmin(aic)), " N =", L)
print("E ratio at p=4,14,30:", [round(float(errs[q] / errs[0]), 4) for q in (4, 14, 30)])

# 예측 오차 신호
a14, errs14 = levinson(R, 14)
e = lfilter(np.concatenate(([1.0], -a14)), [1.0], s)
fig, axes = plt.subplots(2, 1, figsize=(8, 3.8), sharex=True)
t = np.arange(L) / FS * 1000
axes[0].plot(t, s, color=BLUE, lw=1.2)
axes[0].set_ylabel("$s[n]$")
axes[0].set_title("창을 곱한 합성 모음과 14차 예측 오차 신호", loc="left")
axes[1].plot(t, e, color=RED, lw=1.2)
axes[1].set_ylabel("$e[n]$")
axes[1].set_xlabel("시간 (ms)")
fig.tight_layout()
save(fig, ARTICLE, "prediction-error.png")
