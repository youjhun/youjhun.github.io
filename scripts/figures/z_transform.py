"""z 변환 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, pi_ticks, save, setup

ARTICLE = "z-transform"
setup()
th = np.linspace(0, 2 * np.pi, 400)


def zplane(ax, poles=(), zeros=(), roc=None, lim=1.6):
    ax.plot(np.cos(th), np.sin(th), color=GRAY, lw=1, ls="--")
    if roc is not None:
        kind, r = roc
        if kind == "out":
            ax.add_patch(plt.Rectangle((-lim, -lim), 2 * lim, 2 * lim, color=LIGHT, zorder=0))
            ax.add_patch(plt.Circle((0, 0), r, color="white", zorder=0))
        else:
            ax.add_patch(plt.Circle((0, 0), r, color=LIGHT, zorder=0))
        ax.add_patch(plt.Circle((0, 0), r, fill=False, color=BLUE, lw=1.2, zorder=1))
    for p in poles:
        ax.plot(np.real(p), np.imag(p), "x", color=RED, ms=11, mew=2.2, zorder=4)
    for z in zeros:
        ax.plot(np.real(z), np.imag(z), "o", mfc="white", mec=BLUE, ms=10, mew=2, zorder=4)
    ax.axhline(0, color="#999", lw=0.7)
    ax.axvline(0, color="#999", lw=0.7)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.grid(False)


# 그림 1. 같은 식, 다른 수렴영역 → 다른 신호
a = 0.8
fig, axes = plt.subplots(2, 2, figsize=(9, 6.4), gridspec_kw={"width_ratios": [1, 1.6]})
n = np.arange(-10, 11)
for row, (kind, x, title, roc_text) in enumerate(
    [
        ("out", np.where(n >= 0, a**n, 0.0), "x[n] = 0.8ⁿ u[n] (오른쪽으로 뻗는 신호)", "|z| > 0.8"),
        ("in", np.where(n <= -1, -(a**n), 0.0), "x[n] = −0.8ⁿ u[−n−1] (왼쪽으로 뻗는 신호)", "|z| < 0.8"),
    ]
):
    zplane(axes[row, 0], poles=[a], zeros=[0], roc=(kind, a))
    axes[row, 0].set_title(f"수렴영역 {roc_text}", fontsize=11)
    ax = axes[row, 1]
    ax.vlines(n, 0, x, color=BLUE, lw=1.4)
    ax.plot(n, x, "o", color=BLUE, ms=4)
    ax.axhline(0, color="#777", lw=0.7)
    ax.set_title(title, fontsize=11, loc="left")
    ax.set_xlabel("n")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
fig.suptitle("둘 다 X(z) = 1/(1 − 0.8z⁻¹)이다. 수렴영역이 신호를 가른다", fontweight="bold")
fig.tight_layout()
save(fig, ARTICLE, "roc.png")

# 그림 2. 극점 위치가 단위 표본 응답의 모양을 정한다
cases = [
    ([0.5], "극점 0.5: 빨리 줄어든다"),
    ([0.9], "극점 0.9: 천천히 줄어든다"),
    ([-0.8], "극점 −0.8: 부호를 바꾸며 줄어든다"),
    ([0.9 * np.exp(1j * np.pi / 6), 0.9 * np.exp(-1j * np.pi / 6)], "켤레 극점 0.9∠±30°: 진동하며 줄어든다"),
    ([1.05], "극점 1.05 (원 밖): 커진다, 불안정"),
]
n = np.arange(0, 30)
fig, axes = plt.subplots(len(cases), 2, figsize=(9, 9.6), gridspec_kw={"width_ratios": [1, 3.4]})
for (poles, title), (axz, axh) in zip(cases, axes):
    zplane(axz, poles=poles, zeros=[0] * len(poles), lim=1.3)
    if len(poles) == 2:
        axz.text(0.12, 0.12, "2", color=BLUE, fontsize=9)
    axz.set_xticks([])
    axz.set_yticks([])
    # 단위 표본 응답: 분모 다항식으로 직접 재귀
    den = np.real(np.poly(poles))
    h = np.zeros(len(n))
    for i in range(len(n)):
        acc = 1.0 if i == 0 else 0.0
        for k in range(1, len(den)):
            if i - k >= 0:
                acc -= den[k] * h[i - k]
        h[i] = acc
    color = RED if max(abs(p) for p in poles) > 1 else BLUE
    axh.vlines(n, 0, h, color=color, lw=1.3)
    axh.plot(n, h, "o", color=color, ms=3.5)
    axh.axhline(0, color="#777", lw=0.7)
    axh.set_title(title, loc="left", fontsize=11)
axes[-1, 1].set_xlabel("n")
fig.tight_layout()
save(fig, ARTICLE, "pole-positions.png")

# 그림 3. 단위원 위를 돌며 극점·영점까지의 거리를 재면 주파수 응답이 나온다
p, z0 = 0.8, -1.0
w = np.linspace(0, np.pi, 600)
ejw = np.exp(1j * w)
H = (1 + 1 / ejw) / (1 - p / ejw)
fig, (axz, axf) = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [1, 1.6]})
zplane(axz, poles=[p], zeros=[z0], lim=1.4)
w0 = np.pi / 3
e0 = np.exp(1j * w0)
axz.plot([np.real(e0)], [np.imag(e0)], "o", color=ORANGE, ms=8, zorder=5)
axz.annotate("", xy=(e0.real, e0.imag), xytext=(p, 0), arrowprops=dict(arrowstyle="-", color=RED, lw=1.6))
axz.annotate("", xy=(e0.real, e0.imag), xytext=(z0, 0), arrowprops=dict(arrowstyle="-", color=BLUE, lw=1.6))
axz.text(e0.real + 0.08, e0.imag + 0.08, r"$e^{j\omega}$", color=ORANGE, fontsize=13)
axz.text(0.62, 0.42, "극점까지\n거리", color=RED, fontsize=9.5)
axz.text(-0.75, 0.55, "영점까지\n거리", color=BLUE, fontsize=9.5)
axz.set_title("z 평면", fontsize=11)
axf.plot(w, np.abs(H) / np.abs(H[0]), color=BLUE, lw=2)
axf.axvline(w0, color=ORANGE, ls=":", lw=1.2)
axf.set_title(r"$|H(e^{j\omega})|$ = 영점까지 거리 / 극점까지 거리 (ω = 0에서 1로 맞춤)", fontsize=11, loc="left")
pi_ticks(axf, 0, 1, 0.25)
axf.set_xlabel("ω (rad/표본)")
axf.set_ylabel("크기 (상대값)")
fig.tight_layout()
save(fig, ARTICLE, "geometry.png")
