"""피어슨과 스피어먼 상관 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "pearson-spearman"
setup()
rng = np.random.default_rng(11)
n = 60

x1 = rng.normal(0, 1, n)
y1 = x1 + rng.normal(0, 0.6, n)
x2 = rng.uniform(0, 4, n)
y2 = np.exp(1.3 * x2) + rng.normal(0, 0.5, n)
x3 = rng.normal(0, 1, n)
y3 = rng.normal(0, 1, n)
x3 = np.append(x3, 8.0)
y3 = np.append(y3, 8.0)
x4 = rng.uniform(-2, 2, n)
y4 = x4**2 + rng.normal(0, 0.3, n)

cases = [
    (x1, y1, "직선 관계"),
    (x2, y2, "단조롭지만 휘어진 관계"),
    (x3, y3, "관계 없음 + 튀는 점 하나"),
    (x4, y4, "U자 관계"),
]

# 그림 1. 네 가지 경우의 r과 ρ
fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
for ax, (x, y, title) in zip(axes, cases):
    r = stats.pearsonr(x, y)[0]
    rho = stats.spearmanr(x, y)[0]
    ax.scatter(x, y, s=14, color=BLUE, alpha=0.8)
    if title.startswith("관계 없음"):
        ax.scatter(x[-1:], y[-1:], s=60, color=RED, zorder=3)
    ax.set_title(f"{title}\n피어슨 r = {r:.2f} · 스피어먼 ρ = {rho:.2f}", fontsize=10.5)
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
save(fig, ARTICLE, "four-cases.png")

# 그림 2. 스피어먼은 순위로 바꾼 뒤의 피어슨이다
rx, ry = stats.rankdata(x2), stats.rankdata(y2)
fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
axes[0].scatter(x2, y2, s=16, color=BLUE)
axes[0].set_title(f"원래 값: 피어슨 r = {stats.pearsonr(x2, y2)[0]:.2f}", fontsize=11)
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")
axes[1].scatter(rx, ry, s=16, color=TEAL)
axes[1].set_title(f"순위로 바꾼 값: 피어슨 r = {stats.pearsonr(rx, ry)[0]:.2f} (= 스피어먼 ρ)", fontsize=11)
axes[1].set_xlabel("x의 순위")
axes[1].set_ylabel("y의 순위")
fig.tight_layout()
save(fig, ARTICLE, "rank-transform.png")
