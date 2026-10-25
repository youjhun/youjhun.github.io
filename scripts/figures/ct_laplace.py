"""MIT 6.003 연속시간 시스템과 라플라스 변환 문서의 그림.

값은 모두 직접 계산한 것이다. 질량-스프링 예는 ω0 = 1로 둔다.
"""

from math import factorial

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

setup()

# 그림: 1차 피드백의 임펄스 응답과 질량-스프링 급수의 부분합
t = np.linspace(0, 4, 400)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
for p, c in [(0.5, RED), (-0.5, TEAL), (-2, BLUE)]:
    axes[0].plot(t, np.exp(p * t), color=c, lw=2, label=f"$p = {p:g}$")
axes[0].set_xlabel("$t$")
axes[0].set_ylabel("$h(t) = e^{pt}$")
axes[0].set_title("$\\dot y = x + py$의 임펄스 응답", loc="left")
axes[0].legend(fontsize=9.5)

t2 = np.linspace(0, 3 * np.pi, 600)
axes[1].plot(t2, np.sin(t2), color=BLUE, lw=2.4, label="$\\omega_0 \\sin \\omega_0 t$")
for n, c in [(1, GRAY), (3, ORANGE), (6, TEAL)]:
    s = sum((-1) ** l * t2 ** (2 * l + 1) / factorial(2 * l + 1) for l in range(n))
    axes[1].plot(t2, s, color=c, lw=1.4, ls="--", label=f"첫 {n}항")
axes[1].set_ylim(-2, 2)
axes[1].set_xlabel("$\\omega_0 t$")
axes[1].set_ylabel("$h(t)/\\omega_0$")
axes[1].set_title("질량-스프링 임펄스 응답의 급수 부분합", loc="left")
axes[1].legend(fontsize=9, loc="lower left", ncol=2)
fig.tight_layout()
save(fig, "ct-systems-operator", "impulse-responses.png")

# 그림: 수렴영역 세 가지
fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
cases = [
    ("$e^{-t}u(t)$", (-1, 3.2), [-1]),
    ("$-e^{-t}u(-t)$", (-3.2, -1), [-1]),
    ("$e^{-|t|}$", (-1, 1), [-1, 1]),
]
for ax, (name, (lo, hi), poles) in zip(axes, cases):
    ax.add_patch(Rectangle((lo, -3), hi - lo, 6, color=LIGHT, zorder=0))
    for x in (lo, hi):
        if abs(x) < 3:
            ax.axvline(x, color=BLUE, ls="--", lw=1)
    ax.plot(poles, [0] * len(poles), "x", color=RED, ms=10, mew=2)
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(0, color=GRAY, lw=0.8)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("Re $s$")
    ax.set_title(name, loc="left")
    ax.grid(False)
axes[0].set_ylabel("Im $s$")
fig.tight_layout()
save(fig, "laplace-transform", "regions-of-convergence.png")

# 그림: s·e^{-st}의 모양
tt = np.linspace(0, 3, 600)
fig, ax = plt.subplots(figsize=(6, 3.2))
for s, c in [(1, BLUE), (5, TEAL), (25, ORANGE)]:
    ax.plot(tt, s * np.exp(-s * tt), color=c, lw=2, label=f"$s = {s}$")
ax.set_ylim(0, 8)
ax.set_xlabel("$t$")
ax.set_ylabel("$s\\,e^{-st}$")
ax.set_title("$s$에 따른 $s\\,e^{-st}$ (넓이는 모두 1)", loc="left")
ax.legend(fontsize=9.5)
fig.tight_layout()
save(fig, "laplace-transform", "s-exp-kernel.png")
