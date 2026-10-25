"""푸리에 급수, 연속시간 푸리에 변환 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

# 푸리에 급수: 사각파와 삼각파의 부분합
ARTICLE = "fourier-series"
t = np.linspace(-0.5, 1.5, 4001)
square = np.where((t % 1) < 0.5, 0.5, -0.5)
# 삼각파: 사각파(±1/2)를 적분하고 평균을 뺀 것. 진폭 ±1/8
tri = np.cumsum(square) * (t[1] - t[0])
tri -= (tri.max() + tri.min()) / 2


def partial(coef, N):
    s = np.zeros_like(t, dtype=complex)
    for k in range(-N, N + 1):
        if k % 2:
            s += coef(k) * np.exp(1j * 2 * np.pi * k * t)
    return s.real


sq_coef = lambda k: 1 / (1j * np.pi * k)
tri_coef = lambda k: -1 / (2 * np.pi**2 * k**2)

fig, axes = plt.subplots(2, 1, figsize=(9, 5.4), sharex=True)
for ax, coef, ref, name in [(axes[0], sq_coef, square, "사각파"), (axes[1], tri_coef, tri, "삼각파")]:
    ax.plot(t, ref, color=GRAY, lw=1.2, label="원래 신호")
    for N, color in [(1, ORANGE), (5, TEAL), (39, BLUE)]:
        ax.plot(t, partial(coef, N), color=color, lw=1.3, label=f"|k| ≤ {N}까지 더한 합")
    ax.set_title(f"{name}의 푸리에 급수 부분합", loc="left")
axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), fontsize=9.5, ncol=4)
axes[1].set_xlabel("시간 (주기 T = 1)")
fig.tight_layout()
save(fig, ARTICLE, "partial-sums.png")

# RC 저역통과를 지난 사각파: ω0와 1/RC의 비에 따라
fig, axes = plt.subplots(1, 3, figsize=(10, 3.0), sharey=True)
tt = np.linspace(0, 2, 2001)
for ax, ratio, title in [(axes[0], 0.1, "ω₀ = 0.1/RC"), (axes[1], 1, "ω₀ = 1/RC"), (axes[2], 10, "ω₀ = 10/RC")]:
    # 주기 1로 놓고 ω0 = 2π, RC = ratio/ω0
    RC = ratio / (2 * np.pi)
    x = np.where((tt % 1) < 0.5, 0.5, -0.5)
    y = np.zeros_like(tt, dtype=complex)
    for k in range(-301, 302, 2):
        H = 1 / (1 + 1j * 2 * np.pi * k * RC)
        y += (1 / (1j * np.pi * k)) * H * np.exp(1j * 2 * np.pi * k * tt)
    ax.plot(tt, x, color=GRAY, lw=1)
    ax.plot(tt, y.real, color=BLUE, lw=1.8)
    ax.set_title(title, loc="left")
    ax.set_xlabel("시간 (주기 단위)")
axes[0].set_ylabel("전압")
fig.suptitle("RC 저역통과 필터를 지난 사각파", x=0.01, ha="left", fontweight="bold", fontsize=12.5)
fig.tight_layout()
save(fig, ARTICLE, "rc-square-wave.png")

# 연속시간 푸리에 변환: 펄스 폭과 스펙트럼 폭
ARTICLE = "fourier-transform"
w = np.linspace(-4 * np.pi, 4 * np.pi, 4001)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
tt = np.linspace(-3, 3, 1201)
for S, color in [(1, BLUE), (2, RED)]:
    axes[0].plot(tt, (np.abs(tt) <= S).astype(float), color=color, lw=2, label=f"폭 {2 * S}")
    axes[1].plot(w, 2 * S * np.sinc(w * S / np.pi), color=color, lw=2, label=r"$2\sin\omega/\omega$" if S == 1 else r"$2\sin 2\omega/\omega$")
axes[0].set_ylim(-0.1, 1.3)
axes[0].set_title("시간: 높이 1인 사각 펄스", loc="left")
axes[0].set_xlabel("t")
axes[0].legend(fontsize=10)
axes[1].axhline(0, color=GRAY, lw=0.8)
axes[1].set_title("주파수: 푸리에 변환 X(jω)", loc="left")
axes[1].set_xlabel("ω")
axes[1].set_xticks([-4 * np.pi, -2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi, 4 * np.pi])
axes[1].set_xticklabels(["−4π", "−2π", "−π", "0", "π", "2π", "4π"])
axes[1].legend(fontsize=10)
fig.tight_layout()
save(fig, ARTICLE, "pulse-scaling.png")

# 이상적 저역통과 필터의 임펄스 응답
w0 = np.pi
tt = np.linspace(-8, 8, 3201)
h = (w0 / np.pi) * np.sinc(w0 * tt / np.pi)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.2))
ww = np.linspace(-2 * w0, 2 * w0, 801)
axes[0].plot(ww, (np.abs(ww) <= w0).astype(float), color=BLUE, lw=2)
axes[0].set_xticks([-w0, 0, w0])
axes[0].set_xticklabels(["−ω₀", "0", "ω₀"])
axes[0].set_ylim(-0.1, 1.3)
axes[0].set_title("주파수 응답 H(jω)", loc="left")
axes[0].set_xlabel("ω")
axes[1].plot(tt, h, color=RED, lw=2)
axes[1].axhline(0, color=GRAY, lw=0.8)
axes[1].set_title("임펄스 응답 h(t) = sin(ω₀t)/(πt), ω₀ = π", loc="left")
axes[1].set_xlabel("t")
fig.tight_layout()
save(fig, ARTICLE, "ideal-lowpass.png")
