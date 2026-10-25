"""MIT HST.582J 판정과 베이즈 분류기 문서의 그림.

두 가설의 측정값 분포를 분산 1인 정규분포로 둔다: H0은 평균 0, H1은 평균 d = 2.
사전확률과 비용은 예로 정한 값이고, 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()
ARTICLE = "bayes-classifier-detection"
D = 2.0


def threshold(p0, p1, c10=1.0, c01=1.0):
    # p1(x)/p0(x) = exp(D x - D^2/2) > c10 P0 / (c01 P1)
    return D / 2 + np.log(c10 * p0 / (c01 * p1)) / D


def errors(t, p0, p1):
    pf = norm.sf(t)          # P(x > t | H0): 오경보
    pm = norm.cdf(t - D)     # P(x < t | H1): 놓침
    return pf, pm, p0 * pf + p1 * pm


x = np.linspace(-4, 6, 1000)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6), sharey=True)
for ax, (p0, p1) in zip(axes, [(0.5, 0.5), (0.8, 0.2)]):
    a, b = p0 * norm.pdf(x), p1 * norm.pdf(x, D)
    t = threshold(p0, p1)
    ax.plot(x, a, color=BLUE, lw=2, label="$P_0\\,p_0(x)$")
    ax.plot(x, b, color=ORANGE, lw=2, label="$P_1\\,p_1(x)$")
    ax.fill_between(x, 0, a, where=x > t, color=BLUE, alpha=0.25, label="오경보")
    ax.fill_between(x, 0, b, where=x < t, color=ORANGE, alpha=0.3, label="놓침")
    ax.axvline(t, color=GRAY, ls="--", lw=1)
    pf, pm, pe = errors(t, p0, p1)
    ax.set_title(f"$P_0 = {p0}$, $P_1 = {p1}$", loc="left")
    ax.text(t + 0.1, 0.36, f"문턱 {t:.2f}\n$P_E$ = {pe:.3f}", fontsize=9.5, color=GRAY)
    ax.set_xlabel("$x$")
axes[0].set_ylim(0, 0.45)
axes[0].legend(fontsize=9, loc="upper left")
fig.tight_layout()
save(fig, ARTICLE, "decision-regions.png")

# ROC
ts = np.linspace(-4, 6, 500)
fig, ax = plt.subplots(figsize=(4.6, 4.2))
for d, c in [(1.0, GRAY), (2.0, BLUE), (3.0, TEAL)]:
    ax.plot(norm.sf(ts), norm.sf(ts - d), color=c, lw=2, label=f"$d = {d:g}$")
for (p0, p1), m in [((0.5, 0.5), "o"), ((0.8, 0.2), "s")]:
    t = threshold(p0, p1)
    pf, pm, _ = errors(t, p0, p1)
    ax.plot(pf, 1 - pm, m, color=RED, ms=7, label=f"$P_0 = {p0}$의 베이즈 문턱")
ax.plot([0, 1], [0, 1], color=GRAY, lw=0.8, ls=":")
ax.set_xlabel("오경보 확률 $P_F$")
ax.set_ylabel("검출 확률 $P_D$")
ax.set_title("ROC 곡선", loc="left")
ax.set_aspect("equal")
ax.legend(fontsize=8.5, loc="lower right")
fig.tight_layout()
save(fig, ARTICLE, "roc.png")

for p0, p1 in [(0.5, 0.5), (0.8, 0.2)]:
    t = threshold(p0, p1)
    pf, pm, pe = errors(t, p0, p1)
    print(f"P0={p0}: t={t:.3f} PF={pf:.4f} PM={pm:.4f} PE={pe:.4f}")
t = threshold(0.5, 0.5, c10=1.0, c01=4.0)
pf, pm, _ = errors(t, 0.5, 0.5)
print(f"cost C01=4: t={t:.3f} PF={pf:.4f} PM={pm:.4f} Padj1={4*0.5/(4*0.5+0.5):.2f}")
