"""부트스트랩과 표준오차 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "bootstrap"
setup()
rng = np.random.default_rng(3)

# 그림 1. 부트스트랩의 흐름: 표본에서 복원추출을 되풀이한다
sample = np.round(rng.gamma(2.0, 2.0, 10), 1)
fig = plt.figure(figsize=(10, 5.2))
gs = fig.add_gridspec(4, 2, width_ratios=[1.25, 1], hspace=1.05, wspace=0.25)
ax0 = fig.add_subplot(gs[0, 0])
ax0.scatter(sample, np.zeros_like(sample), s=60, color=BLUE, zorder=3)
ax0.set_title(f"원래 표본 (n = 10, 평균 {sample.mean():.2f})", loc="left", fontsize=11)
ax0.tick_params(labelbottom=False)
for i in range(3):
    ax = fig.add_subplot(gs[i + 1, 0], sharex=ax0)
    idx = rng.integers(0, len(sample), len(sample))
    vals, counts = np.unique(sample[idx], return_counts=True)
    for v, c in zip(vals, counts):
        ax.scatter([v] * c, np.arange(c) * 0.35, s=40, color=TEAL, zorder=3)
    ax.set_title(f"부트스트랩 표본 {i + 1} (평균 {sample[idx].mean():.2f}): 같은 값이 여러 번 뽑힐 수 있다", loc="left", fontsize=10)
    if i < 2:
        ax.tick_params(labelbottom=False)
for ax in fig.axes:
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylim(-0.4, 1.2)
ax_h = fig.add_subplot(gs[:, 1])
B = 10000
boot = sample[rng.integers(0, len(sample), (B, len(sample)))].mean(axis=1)
ax_h.hist(boot, bins=40, color=TEAL, edgecolor="white")
se = boot.std(ddof=1)
lo, hi = np.percentile(boot, [2.5, 97.5])
ax_h.axvline(lo, color=ORANGE, ls="--")
ax_h.axvline(hi, color=ORANGE, ls="--")
ax_h.set_title(f"부트스트랩 평균 {B:,}개의 분포\n표준편차 = SE ≈ {se:.2f}, 95% 구간 [{lo:.2f}, {hi:.2f}]", fontsize=11)
ax_h.set_xlabel("평균")
ax_h.set_yticks([])
save(fig, ARTICLE, "resampling.png")

# 그림 2. 표준편차는 그대로, 표준오차는 1/√n으로 줄어든다
ns = np.array([5, 10, 20, 50, 100, 200, 500, 1000])
sd, se_emp = [], []
for n in ns:
    data = rng.normal(0, 1, (4000, n))
    sd.append(data.std(axis=1, ddof=1).mean())
    se_emp.append(data.mean(axis=1).std(ddof=1))
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.semilogx(ns, sd, "o-", color=GRAY, label="자료의 표준편차 (SD)")
ax.semilogx(ns, se_emp, "o-", color=BLUE, label="표본평균의 표준편차 = 표준오차 (SE)")
ax.semilogx(ns, 1 / np.sqrt(ns), ":", color=BLUE, lw=1.2, label="σ/√n")
ax.set_xlabel("표본 크기 n")
ax.set_ylabel("크기")
ax.set_title("SD는 자료의 퍼짐, SE는 추정값의 흔들림", loc="left")
ax.legend(fontsize=9.5)
save(fig, ARTICLE, "sd-vs-se.png")

# 그림 3. 상관계수의 표본분포: 모집단에서 새로 뽑은 것 대 한 표본의 부트스트랩
rho, n = 0.5, 30
cov = [[1, rho], [rho, 1]]
true_r = []
for _ in range(10000):
    x = rng.multivariate_normal([0, 0], cov, n)
    true_r.append(np.corrcoef(x.T)[0, 1])
x = rng.multivariate_normal([0, 0], cov, n)
r_hat = np.corrcoef(x.T)[0, 1]
boot_r = []
for _ in range(10000):
    idx = rng.integers(0, n, n)
    boot_r.append(np.corrcoef(x[idx].T)[0, 1])
fig, ax = plt.subplots(figsize=(8, 3.6))
bins = np.linspace(-0.3, 1, 60)
ax.hist(true_r, bins=bins, density=True, color=GRAY, alpha=0.6, label=f"모집단에서 새로 뽑은 표본들 (SD {np.std(true_r):.3f})")
ax.hist(boot_r, bins=bins, density=True, histtype="step", color=BLUE, lw=2, label=f"한 표본의 부트스트랩 (SD {np.std(boot_r):.3f})")
ax.axvline(rho, color=RED, ls="--", lw=1.2, label="참값 ρ = 0.5")
ax.axvline(r_hat, color=BLUE, ls=":", lw=1.4, label=f"이 표본의 r = {r_hat:.2f}")
ax.set_xlabel("상관계수 r (n = 30)")
ax.set_yticks([])
ax.set_title("현실에선 회색을 볼 수 없다. 파란 선이 그 대역이다", loc="left")
ax.legend(fontsize=9, loc="upper left")
save(fig, ARTICLE, "correlation-se.png")
