"""다중비교와 FDR 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "multiple-comparisons-fdr"
setup()
rng = np.random.default_rng(5)

# 그림 1. 검정을 여러 번 하면 한 번이라도 헛짚을 확률이 빠르게 커진다
m = np.arange(1, 101)
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.plot(m, 1 - 0.95**m, color=RED, lw=2)
for mm in (1, 10, 20, 50):
    v = 1 - 0.95**mm
    ax.plot(mm, v, "o", color=RED)
    ax.annotate(f"{mm}번: {v:.0%}", (mm, v), (mm + 3, v - 0.09), fontsize=10)
ax.set_xlabel("검정 횟수 m (모두 효과 없음, 각각 α = 0.05)")
ax.set_ylabel("한 번 이상 거짓 양성")
ax.set_ylim(0, 1.05)
ax.set_title("1 − 0.95ᵐ: 20번이면 64%", loc="left")
save(fig, ARTICLE, "fwer.png")


def simulate(m=50, m1=10, effect=3.0):
    z = rng.normal(0, 1, m)
    truth = np.zeros(m, bool)
    truth[:m1] = True
    z[truth] += effect
    p = 2 * stats.norm.sf(np.abs(z))
    return p, truth


def bh(p, q):
    m = len(p)
    order = np.argsort(p)
    passed = p[order] <= q * np.arange(1, m + 1) / m
    k = np.max(np.nonzero(passed)[0]) + 1 if passed.any() else 0
    reject = np.zeros(m, bool)
    reject[order[:k]] = True
    return reject, k


# 그림 2. BH 절차: 정렬한 p-value를 기울어진 선과 비교한다
p, truth = simulate()
q = 0.05
order = np.argsort(p)
ranks = np.arange(1, len(p) + 1)
reject, k = bh(p, q)
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.plot(ranks, q * ranks / len(p), color=BLUE, lw=1.6, label="BH 기준선 (k/m)·q")
ax.axhline(q / len(p), color=ORANGE, lw=1.4, ls="--", label="Bonferroni 기준 q/m")
ax.axhline(q, color=GRAY, lw=1, ls=":", label="보정 없음 0.05")
colors = [TEAL if truth[i] else GRAY for i in order]
ax.scatter(ranks, p[order], c=colors, s=28, zorder=3)
ax.axvline(k + 0.5, color=RED, lw=1, ls="-.")
ax.text(k + 1, 0.0035, f"여기까지 {k}개 기각", color=RED)
ax.set_yscale("log")
ax.set_xlim(0, 30)
ax.set_ylim(1e-6, 0.3)
ax.set_xlabel("p-value 순위 k (작은 것부터)")
ax.set_ylabel("p-value (로그)")
ax.set_title("검정 50개 중 10개만 진짜 효과 (초록 점)", loc="left")
ax.legend(fontsize=9, loc="lower right")
save(fig, ARTICLE, "bh-procedure.png")

# 그림 3. 1,000번 반복: 세 방법의 발견과 헛짚음
res = {"보정 없음": [], "Bonferroni": [], "BH (q = 0.05)": []}
for _ in range(1000):
    p, truth = simulate()
    rej = {
        "보정 없음": p < 0.05,
        "Bonferroni": p < 0.05 / len(p),
        "BH (q = 0.05)": bh(p, 0.05)[0],
    }
    for name, r in rej.items():
        tp = np.sum(r & truth)
        fp = np.sum(r & ~truth)
        fdp = fp / max(r.sum(), 1)
        res[name].append((tp, fp, fdp))
names = list(res)
tp = [np.mean([x[0] for x in res[nm]]) for nm in names]
fp = [np.mean([x[1] for x in res[nm]]) for nm in names]
fdr = [np.mean([x[2] for x in res[nm]]) for nm in names]
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
y = np.arange(len(names))
axes[0].barh(y - 0.2, tp, height=0.38, color=TEAL, label="진짜 발견 (10개 중)")
axes[0].barh(y + 0.2, fp, height=0.38, color=RED, label="거짓 발견 (40개 중)")
for i in range(len(names)):
    axes[0].text(tp[i] + 0.1, i - 0.2, f"{tp[i]:.1f}", va="center", fontsize=9.5)
    axes[0].text(fp[i] + 0.1, i + 0.2, f"{fp[i]:.2f}", va="center", fontsize=9.5)
axes[0].set_yticks(y)
axes[0].set_yticklabels(names)
axes[0].invert_yaxis()
axes[0].legend(fontsize=9, loc="lower right")
axes[0].set_title("평균 발견 수", loc="left")
axes[1].barh(y, fdr, color=BLUE, height=0.5)
axes[1].axvline(0.05, color=ORANGE, ls="--")
for i in range(len(names)):
    axes[1].text(fdr[i] + 0.003, i, f"{fdr[i]:.3f}", va="center", fontsize=9.5)
axes[1].set_yticks(y)
axes[1].set_yticklabels(names)
axes[1].invert_yaxis()
axes[1].set_title("발견 중 거짓의 비율 (평균 = FDR)", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "methods.png")
print(dict(zip(names, zip(tp, fp, fdr))))
