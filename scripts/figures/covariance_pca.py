"""공분산 행렬, PCA와 SVD 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

setup()
rng = np.random.default_rng(21)


def ellipse(ax, cov, mean=(0, 0), nsig=2, **kw):
    vals, vecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    w, h = 2 * nsig * np.sqrt(vals[1]), 2 * nsig * np.sqrt(vals[0])
    ax.add_patch(Ellipse(mean, w, h, angle=angle, fill=False, **kw))


# 공분산 그림 1. 세 가지 공분산 행렬과 그 모양
covs = [
    (np.array([[1.0, 0.8], [0.8, 1.0]]), "양의 공분산"),
    (np.array([[1.0, 0.0], [0.0, 1.0]]), "공분산 0"),
    (np.array([[1.0, -0.6], [-0.6, 0.5]]), "음의 공분산"),
]
fig, axes = plt.subplots(1, 3, figsize=(11, 3.9))
for ax, (C, title) in zip(axes, covs):
    X = rng.multivariate_normal([0, 0], C, 400)
    S = np.cov(X.T)
    ax.scatter(X[:, 0], X[:, 1], s=6, color=BLUE, alpha=0.5)
    ellipse(ax, S, color=RED, lw=1.8)
    ax.set_title(f"{title}\nΣ ≈ [[{S[0,0]:.2f}, {S[0,1]:.2f}], [{S[1,0]:.2f}, {S[1,1]:.2f}]]", fontsize=10.5)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.set_xlabel("x₁")
axes[0].set_ylabel("x₂")
save(fig, "covariance-matrix", "shapes.png")

# 공분산 그림 2. 고유벡터는 타원의 축, 고유값은 그 방향의 분산
C = np.array([[2.0, 1.2], [1.2, 1.0]])
X = rng.multivariate_normal([0, 0], C, 600)
S = np.cov(X.T)
vals, vecs = np.linalg.eigh(S)
fig, ax = plt.subplots(figsize=(5.6, 5))
ax.scatter(X[:, 0], X[:, 1], s=6, color=GRAY, alpha=0.5)
ellipse(ax, S, color=RED, lw=1.5, nsig=1)
for i, color in zip([1, 0], [BLUE, TEAL]):
    v = vecs[:, i] * np.sqrt(vals[i])
    ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4))
    ax.text(v[0] * 1.15, v[1] * 1.15 + (0.15 if i == 1 else -0.35), f"고유값 {vals[i]:.2f}", color=color, fontsize=10.5)
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect("equal")
ax.set_title("화살표: 고유벡터 × √고유값 (빨간 타원은 1σ)", fontsize=11)
save(fig, "covariance-matrix", "eigen.png")

# 공분산 그림 3. 채널 × 시간 신호의 공분산 행렬 (합성 데이터)
fs, T = 250, 4
t = np.arange(fs * T) / fs
alpha = np.sin(2 * np.pi * 10 * t) * (1 + 0.3 * np.sin(2 * np.pi * 0.5 * t))
drift = np.cumsum(rng.normal(0, 0.05, len(t)))
mix = np.array([[1.0, 0.1], [0.8, 0.2], [0.3, 0.9], [0.1, 1.0]])
sig = mix @ np.vstack([alpha, drift]) + rng.normal(0, 0.3, (4, len(t)))
names = ["채널 1", "채널 2", "채널 3", "채널 4"]
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"width_ratios": [1.7, 1]})
for i in range(4):
    axes[0].plot(t[:500], sig[i, :500] - 3 * i, color=[BLUE, BLUE, TEAL, TEAL][i], lw=0.8)
axes[0].set_yticks([-3 * i for i in range(4)])
axes[0].set_yticklabels(names)
axes[0].set_xlabel("시간 (s)")
axes[0].set_title("합성 신호: 1·2는 10 Hz 성분을, 3·4는 느린 표류를 주로 공유", loc="left", fontsize=10.5)
Xc = sig - sig.mean(axis=1, keepdims=True)
Cm = Xc @ Xc.T / (Xc.shape[1] - 1)
Rm = Cm / np.sqrt(np.outer(np.diag(Cm), np.diag(Cm)))
im = axes[1].imshow(Rm, cmap="RdBu_r", vmin=-1, vmax=1)
for i in range(4):
    for j in range(4):
        axes[1].text(j, i, f"{Rm[i, j]:.2f}", ha="center", va="center", fontsize=10)
axes[1].set_xticks(range(4))
axes[1].set_yticks(range(4))
axes[1].set_xticklabels(names, fontsize=9)
axes[1].set_yticklabels(names, fontsize=9)
axes[1].set_title("상관 행렬 (공분산을 표준화)", fontsize=11)
axes[1].grid(False)
fig.tight_layout()
save(fig, "covariance-matrix", "channels.png")

# PCA 그림 1. 주성분 방향과 첫 주성분으로의 투영
C = np.array([[3.0, 1.6], [1.6, 1.4]])
X = rng.multivariate_normal([0, 0], C, 120)
Xc = X - X.mean(axis=0)
U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
v1, v2 = Vt[0], Vt[1]
proj = np.outer(Xc @ v1, v1)
fig, ax = plt.subplots(figsize=(6.2, 5))
for p, q in zip(Xc[:40], proj[:40]):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=0.6)
ax.scatter(Xc[:, 0], Xc[:, 1], s=10, color=BLUE, alpha=0.6, label="중심을 뺀 자료")
ax.scatter(proj[:40, 0], proj[:40, 1], s=10, color=ORANGE, label="PC1 위로의 투영")
lam = s**2 / (len(X) - 1)
for v, l, color, name in [(v1, lam[0], RED, "PC1"), (v2, lam[1], TEAL, "PC2")]:
    ax.annotate("", xy=2 * np.sqrt(l) * v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4))
    ax.text(*(2.25 * np.sqrt(l) * v), f"{name} (분산 {l:.2f})", color=color, fontsize=10.5)
ax.set_aspect("equal")
ax.set_xlim(-6, 6)
ax.set_ylim(-4.5, 4.5)
ax.legend(fontsize=9, loc="lower right")
ax.set_title("PC1은 분산이 가장 큰 방향, 투영은 거리를 가장 덜 잃는 방향", fontsize=10.5)
save(fig, "pca-svd", "directions.png")

# PCA 그림 2. 설명 분산 비율 (잠재 요인 3개 + 잡음인 10차원 자료)
latent = rng.normal(0, 1, (500, 3)) * np.array([3.0, 2.0, 1.2])
W = rng.normal(0, 1, (3, 10))
Y = latent @ W + rng.normal(0, 0.8, (500, 10))
Yc = Y - Y.mean(axis=0)
s = np.linalg.svd(Yc, compute_uv=False)
ev = s**2 / np.sum(s**2)
fig, ax = plt.subplots(figsize=(7.5, 3.4))
ax.bar(np.arange(1, 11), ev, color=[BLUE] * 3 + [GRAY] * 7)
ax.plot(np.arange(1, 11), np.cumsum(ev), "o-", color=ORANGE, label="누적")
ax.set_xticks(np.arange(1, 11))
ax.set_xlabel("주성분 번호")
ax.set_ylabel("설명 분산 비율")
ax.set_title(f"숨은 요인 3개로 만든 10차원 자료: 앞의 3개가 {np.cumsum(ev)[2]:.0%}", loc="left", fontsize=11)
ax.legend(fontsize=9.5)
save(fig, "pca-svd", "scree.png")

# PCA 그림 3. 특잇값 몇 개만으로 다시 만든 그림
h, w = 120, 160
yy, xx = np.mgrid[0:h, 0:w]
img = 0.2 + 0.6 * ((xx - 50) ** 2 + (yy - 60) ** 2 < 35**2)
img += 0.5 * ((xx > 95) & (xx < 145) & (yy > 25) & (yy < 95))
img += 0.25 * np.sin(xx / 7.0) * (yy > 100)
img += 0.15 * ((xx + yy) % 40 < 4)
U, s, Vt = np.linalg.svd(img, full_matrices=False)
fig, axes = plt.subplots(1, 4, figsize=(12, 2.8))
for ax, k in zip(axes, [1, 3, 10, 40]):
    rec = (U[:, :k] * s[:k]) @ Vt[:k]
    err = np.linalg.norm(img - rec) / np.linalg.norm(img)
    ax.imshow(rec, cmap="gray", vmin=0, vmax=1.5)
    ax.set_title(f"특잇값 {k}개 (상대 오차 {err:.1%})", fontsize=10.5)
    ax.axis("off")
fig.suptitle(f"120×160 그림 (특잇값 최대 {min(h, w)}개)", fontweight="bold", y=1.04)
fig.tight_layout()
save(fig, "pca-svd", "low-rank.png")
