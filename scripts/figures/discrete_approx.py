"""MIT 6.003 연속시간 시스템의 이산 근사 문서의 그림.

새는 탱크 τ ẏ = x − y의 계단 응답을 전진·후진 오일러로 근사하고, 세 근사법이 s 평면의
왼쪽 반평면을 z 평면 어디로 옮기는지 그린다. 값은 모두 직접 계산한 것이다.
질량-스프링 극점은 ω0 T = 0.5로 둔다.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

setup()
ARTICLE = "discrete-approximation"


def forward(r, n):
    y = np.zeros(n)
    for k in range(n - 1):
        y[k + 1] = (1 - r) * y[k] + r
    return y


def backward(r, n):
    y = np.zeros(n)
    prev = 0.0
    for k in range(n):
        y[k] = (prev + r) / (1 + r)
        prev = y[k]
    return y


ratios = [0.3, 1, 1.5, 2]
fig, axes = plt.subplots(2, 4, figsize=(11, 4.6), sharey=True)
tc = np.linspace(0, 6, 300)
for j, r in enumerate(ratios):
    n = int(6 / r) + 1
    tn = np.arange(n) * r
    for i, (f, c, name) in enumerate([(forward, RED, "전진 오일러"), (backward, TEAL, "후진 오일러")]):
        ax = axes[i, j]
        ax.plot(tc, 1 - np.exp(-tc), color=GRAY, lw=1.5)
        ax.plot(tn, f(r, n), "o", color=c, ms=4.5)
        ax.vlines(tn, 0, f(r, n), color=c, lw=1)
        ax.set_ylim(-0.2, 2.2)
        ax.set_xlim(-0.2, 6.2)
        if i == 0:
            ax.set_title(f"$T/\\tau = {r:g}$", loc="left")
        if j == 0:
            ax.set_ylabel(name)
        if i == 1:
            ax.set_xlabel("$t/\\tau$")
fig.tight_layout()
save(fig, ARTICLE, "leaky-tank-steps.png")

# s 평면의 왼쪽 반평면이 옮겨 가는 곳
fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6))
th = np.linspace(0, 2 * np.pi, 400)
w0T = 0.5
maps = [
    ("전진 오일러  $z = 1 + sT$", lambda s: 1 + s),
    ("후진 오일러  $z = 1/(1 - sT)$", lambda s: 1 / (1 - s)),
    ("사다리꼴  $z = (1 + sT/2)/(1 - sT/2)$", lambda s: (1 + s / 2) / (1 - s / 2)),
]
for k, (ax, (name, f)) in enumerate(zip(axes, maps)):
    if k == 0:
        ax.add_patch(Rectangle((-3, -3), 4, 6, color=LIGHT, zorder=0))
    elif k == 1:
        ax.add_patch(Circle((0.5, 0), 0.5, color=LIGHT, zorder=0))
    else:
        ax.add_patch(Circle((0, 0), 1, color=LIGHT, zorder=0))
    ax.plot(np.cos(th), np.sin(th), color=BLUE, lw=1.2, ls="--")
    zp = f(np.array([1j * w0T, -1j * w0T]))
    ax.plot(zp.real, zp.imag, "x", color=RED, ms=9, mew=2)
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(0, color=GRAY, lw=0.8)
    ax.set_xlim(-1.6, 1.8)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.grid(False)
    ax.set_xlabel("Re $z$")
    ax.set_title(name, loc="left", fontsize=10.5)
axes[0].set_ylabel("Im $z$")
fig.tight_layout()
save(fig, ARTICLE, "s-to-z-maps.png")

for name, f in maps:
    z = f(1j * w0T)
    print(name, abs(z))
for r in ratios:
    print(r, "forward pole", 1 - r, "backward pole", round(1 / (1 + r), 3))
