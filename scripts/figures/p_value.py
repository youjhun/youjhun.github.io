"""p-value 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "p-value"
setup()

# 그림 1. 동전 100번에 앞면 60번: 귀무분포와 p-value
n, k_obs = 100, 60
k = np.arange(0, n + 1)
pmf = stats.binom.pmf(k, n, 0.5)
extreme = np.abs(k - 50) >= abs(k_obs - 50)
p_two = pmf[extreme].sum()
fig, ax = plt.subplots(figsize=(8.5, 3.6))
ax.bar(k[~extreme], pmf[~extreme], color=GRAY, width=0.85)
ax.bar(k[extreme], pmf[extreme], color=RED, width=0.85, label=f"관측값만큼 이상 극단적인 쪽 (합 = {p_two:.3f})")
ax.axvline(k_obs, color=ORANGE, lw=1.5, ls="--")
ax.text(k_obs + 1, pmf.max() * 0.85, "관측: 앞면 60번", color=ORANGE)
ax.set_xlim(25, 75)
ax.set_xlabel("앞면 횟수 (100번 던짐)")
ax.set_ylabel("확률")
ax.set_title("귀무가설 '공정한 동전'이 맞다면 나올 결과의 분포", loc="left")
ax.legend(loc="upper left", fontsize=9.5)
save(fig, ARTICLE, "coin-null.png")

# 그림 2. 효과가 없을 때 p-value는 고르게 퍼진다. 효과가 있으면 0 쪽으로 몰린다
rng = np.random.default_rng(1)
reps, m = 20000, 20
ps = {}
for d in (0.0, 0.8):
    a = rng.normal(0, 1, (reps, m))
    b = rng.normal(d, 1, (reps, m))
    ps[d] = stats.ttest_ind(a, b, axis=1).pvalue
fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.4), sharey=True)
bins = np.linspace(0, 1, 21)
for ax, d, title, color in [(axes[0], 0.0, "효과 없음 (귀무가설이 참)", GRAY), (axes[1], 0.8, "효과 있음 (차이 0.8 표준편차)", BLUE)]:
    w = np.ones_like(ps[d]) / len(ps[d])
    ax.hist(ps[d], bins=bins, weights=w, color=color, edgecolor="white")
    ax.axvline(0.05, color=RED, ls="--", lw=1.2)
    frac = np.mean(ps[d] < 0.05)
    ax.set_title(f"{title}\np < 0.05인 비율: {frac:.1%}", fontsize=11)
    ax.set_xlabel("p-value")
axes[0].set_ylabel("실험 비율")
fig.suptitle("두 집단 각 20명, t-검정 20,000번 반복", fontweight="bold", y=1.04)
fig.tight_layout()
save(fig, ARTICLE, "p-distribution.png")

# 그림 3. 같은 작은 효과도 표본이 커지면 p-value가 한없이 작아진다
d = 0.1
ns = np.unique(np.logspace(1, 4.3, 22).astype(int))
med = []
for m in ns:
    a = rng.normal(0, 1, (400, m))
    b = rng.normal(d, 1, (400, m))
    med.append(np.median(stats.ttest_ind(a, b, axis=1).pvalue))
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.loglog(ns, med, "o-", color=BLUE)
ax.axhline(0.05, color=RED, ls="--", lw=1.2)
ax.text(ns[0], 0.06, "0.05", color=RED)
ax.set_xlabel("집단당 표본 수")
ax.set_ylabel("p-value (중앙값)")
ax.set_title("효과 크기는 0.1 표준편차로 그대로인데 p-value만 작아진다", loc="left")
save(fig, ARTICLE, "sample-size.png")
print(f"two-sided p = {p_two:.4f}")
