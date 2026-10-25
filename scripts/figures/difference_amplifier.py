"""차동 증폭기와 CMRR 문서의 그림."""

import itertools

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

ARTICLE = "difference-amplifier-cmrr"
setup()


def gains(R1, R2, R3, R4):
    """op-amp 하나짜리 차동 증폭기. V1은 R1을 거쳐 반전 입력에, V2는 R3·R4 분압을 거쳐 비반전 입력에 들어간다."""
    a1 = -R2 / R1
    a2 = (R4 / (R3 + R4)) * (1 + R2 / R1)
    ad = (a2 - a1) / 2  # V1 = Vcm − Vd/2, V2 = Vcm + Vd/2
    acm = a1 + a2
    return ad, acm


# 그림 2. 저항 허용오차와 최악의 CMRR
eps = np.logspace(-4, -1, 60)
fig, ax = plt.subplots(figsize=(8, 3.8))
for G, color in [(1, GRAY), (10, BLUE), (100, RED)]:
    worst = []
    for e in eps:
        best = np.inf
        for s in itertools.product([-1, 1], repeat=4):
            R1, R2, R3, R4 = 1 * (1 + s[0] * e), G * (1 + s[1] * e), 1 * (1 + s[2] * e), G * (1 + s[3] * e)
            ad, acm = gains(R1, R2, R3, R4)
            best = min(best, abs(ad / acm) if acm != 0 else np.inf)
        worst.append(20 * np.log10(best))
    ax.semilogx(eps * 100, worst, color=color, lw=2, label=f"이득 {G}")
ax.set_xlabel("저항 허용오차 (%)")
ax.set_ylabel("최악의 CMRR (dB)")
ax.set_title("저항 네 개의 오차가 가장 나쁘게 겹칠 때의 CMRR", loc="left")
ax.legend(loc="upper right", fontsize=10)
save(fig, ARTICLE, "cmrr-tolerance.png")

# 그림 1. 두 전극에 같이 들어온 60 Hz 간섭이 출력에 얼마나 남는가 (예시 값)
fs = 2000
t = np.arange(0, 2, 1 / fs)
beat = np.zeros_like(t)
for t0 in np.arange(0.2, 2, 0.8):  # 75 bpm 간격의 단순한 R파 모양
    beat += 1.0 * np.exp(-((t - t0) / 0.012) ** 2) - 0.15 * np.exp(-((t - t0 - 0.03) / 0.015) ** 2)
    beat += 0.25 * np.exp(-((t - t0 - 0.25) / 0.05) ** 2)
vd = 1e-3 * beat  # 차동 신호 약 1 mV
vcm = 0.1 * np.sin(2 * np.pi * 60 * t)  # 공통모드 간섭 100 mV
G = 1000
fig, axes = plt.subplots(4, 1, figsize=(9, 6.4), sharex=True)
axes[0].plot(t, (vcm + vd / 2) * 1e3, color=GRAY, lw=0.8)
axes[0].set_title("한 전극의 전압: 100 mV, 60 Hz 공통모드 간섭에 묻힌 심전도 (예시, 두 전극 차이 1 mV)", loc="left", fontsize=10.5)
axes[0].set_ylabel("mV")
for ax, cmrr_db, color in [(axes[1], 40, RED), (axes[2], 60, ORANGE), (axes[3], 80, BLUE)]:
    acm = G / 10 ** (cmrr_db / 20)
    out = G * vd + acm * vcm
    ax.plot(t, out, color=color, lw=1)
    ax.set_title(f"출력 (차동 이득 {G}, CMRR {cmrr_db} dB → 간섭 {acm * 0.1 * 1e3:.0f} mV)", loc="left", fontsize=10.5)
    ax.set_ylabel("V")
axes[3].set_xlabel("시간 (s)")
fig.tight_layout()
save(fig, ARTICLE, "cmrr-ecg.png")
