"""CSP, LDA, 데이터 누수 문서의 그림. 모든 자료는 합성이다."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

setup()
rng = np.random.default_rng(42)


def ellipse(ax, cov, mean, nsig=2, **kw):
    vals, vecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    ax.add_patch(Ellipse(mean, 2 * nsig * np.sqrt(vals[1]), 2 * nsig * np.sqrt(vals[0]), angle=angle, fill=False, **kw))


def gen_eig(Ca, Cb):
    """Ca w = λ (Ca + Cb) w 를 푼다. λ 오름차순."""
    M = Ca + Cb
    d, E = np.linalg.eigh(M)
    P = E @ np.diag(d**-0.5) @ E.T  # 백색화
    lam, V = np.linalg.eigh(P @ Ca @ P.T)
    W = P.T @ V
    return lam, W


# ── CSP 그림 1. 두 채널, 두 조건: 분산 비가 가장 큰 방향
Ca = np.array([[1.0, 0.75], [0.75, 1.0]]) * 1.2
Cb = np.array([[1.0, -0.5], [-0.5, 1.0]]) * 0.9
Xa = rng.multivariate_normal([0, 0], Ca, 300)
Xb = rng.multivariate_normal([0, 0], Cb, 300)
lam, W = gen_eig(np.cov(Xa.T), np.cov(Xb.T))
fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
ax = axes[0]
ax.scatter(Xa[:, 0], Xa[:, 1], s=6, color=BLUE, alpha=0.45, label="조건 A의 표본")
ax.scatter(Xb[:, 0], Xb[:, 1], s=6, color=ORANGE, alpha=0.45, label="조건 B의 표본")
ellipse(ax, np.cov(Xa.T), (0, 0), color=BLUE, lw=1.8)
ellipse(ax, np.cov(Xb.T), (0, 0), color=ORANGE, lw=1.8)
for j, color, name in [(0, ORANGE, "w₁ (B 분산이 큰 쪽)"), (1, BLUE, "w₂ (A 분산이 큰 쪽)")]:
    v = W[:, j] / np.linalg.norm(W[:, j]) * 3
    ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4))
    ax.text(v[0] * 1.08, v[1] * 1.08, name, color=color, fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85), zorder=5)
ax.set_aspect("equal")
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.5, 4.5)
ax.set_xlabel("채널 1")
ax.set_ylabel("채널 2")
ax.legend(fontsize=9, loc="upper left", frameon=True, framealpha=0.9)
ax.set_title("CSP 방향: 한 조건의 분산은 크고 다른 조건은 작다", fontsize=11)
ax = axes[1]
for j, (X, color, name) in enumerate([(Xa, BLUE, "A"), (Xb, ORANGE, "B")]):
    pass
proj = {name: X @ W for name, X in [("A", Xa), ("B", Xb)]}
labels = ["w₁ 방향 분산", "w₂ 방향 분산"]
va = [np.var(proj["A"][:, 0]), np.var(proj["A"][:, 1])]
vb = [np.var(proj["B"][:, 0]), np.var(proj["B"][:, 1])]
x = np.arange(2)
ax.bar(x - 0.18, va, width=0.36, color=BLUE, label="조건 A")
ax.bar(x + 0.18, vb, width=0.36, color=ORANGE, label="조건 B")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("투영한 신호의 분산 (두 조건의 합이 1이 되게 맞춤)")
ax.legend(fontsize=9.5)
ax.set_title("두 방향에서 분산의 크고 작음이 뒤바뀐다", fontsize=11)
save(fig, "csp", "two-channel.png")

# ── CSP 그림 2. 8채널 합성 운동상상 자료: 로그 분산 특징이 CSP 뒤에 갈라진다
fs, T, n_trials, C = 250, 2.0, 60, 8
t = np.arange(int(fs * T)) / fs
mix = rng.normal(0, 1, (C, C))  # 소스 → 채널 섞임
left, right = 2, 5  # 이 소스의 리듬이 조건에 따라 약해진다(ERD)


def trial(cond):
    src = rng.normal(0, 1, (C, len(t)))
    for k in (left, right):
        amp = 3.0
        if (cond == "A" and k == left) or (cond == "B" and k == right):
            amp *= 0.35  # 이 조건에서는 해당 리듬이 줄어든다
        src[k] += amp * np.sin(2 * np.pi * 11 * t + rng.uniform(0, 2 * np.pi))
    return mix @ src


XA = np.array([trial("A") for _ in range(n_trials)])
XB = np.array([trial("B") for _ in range(n_trials)])


def mean_cov(X):
    return np.mean([x @ x.T / x.shape[1] for x in X], axis=0)


lam, W = gen_eig(mean_cov(XA[:40]), mean_cov(XB[:40]))  # 학습 시행 40개로만 필터를 구한다
Wsel = W[:, [0, -1]]


def logvar(X, Wm):
    return np.array([np.log(np.var(Wm.T @ x, axis=1)) for x in X])


raw_pair = np.eye(C)[:, [left, right]]
raw_pair = np.eye(C)[:, [0, 1]]
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, Wm, title, xl in [
    (axes[0], np.eye(C)[:, [0, 1]], "원래 채널 두 개의 로그 분산", ("채널 1", "채널 2")),
    (axes[1], Wsel, "CSP 필터 두 개(양 끝 고유값)의 로그 분산", ("CSP 1", "CSP 2")),
]:
    fa, fb = logvar(XA[40:], Wm), logvar(XB[40:], Wm)
    ax.scatter(fa[:, 0], fa[:, 1], color=BLUE, s=28, label="조건 A (시험 시행)")
    ax.scatter(fb[:, 0], fb[:, 1], color=ORANGE, s=28, marker="s", label="조건 B (시험 시행)")
    ax.set_xlabel(f"log var({xl[0]})")
    ax.set_ylabel(f"log var({xl[1]})")
    ax.set_title(title, fontsize=11)
axes[1].legend(fontsize=9)
fig.suptitle("합성 8채널 자료: 필터는 학습 시행 40개로 구하고, 점은 따로 둔 시험 시행 20개", fontweight="bold", y=1.03, fontsize=11)
fig.tight_layout()
save(fig, "csp", "features.png")

# ── LDA 그림 1. 평균 차이 방향 대 피셔 방향
S = np.array([[3.0, 2.2], [2.2, 2.0]])
mA, mB = np.array([0.0, 0.0]), np.array([1.6, -0.6])
A = rng.multivariate_normal(mA, S, 300)
B = rng.multivariate_normal(mB, S, 300)
Sw = np.cov(A.T) + np.cov(B.T)
w_fisher = np.linalg.solve(Sw, B.mean(0) - A.mean(0))
w_naive = B.mean(0) - A.mean(0)
fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.9), gridspec_kw={"width_ratios": [1.2, 1, 1]})
ax = axes[0]
ax.scatter(A[:, 0], A[:, 1], s=6, color=BLUE, alpha=0.45, label="클래스 1")
ax.scatter(B[:, 0], B[:, 1], s=6, color=ORANGE, alpha=0.45, label="클래스 2")
c = (A.mean(0) + B.mean(0)) / 2
for w, color, name in [(w_naive, GRAY, "평균 차이 방향"), (w_fisher, RED, "피셔 방향")]:
    u = w / np.linalg.norm(w) * 3.2
    ax.annotate("", xy=c + u, xytext=c - u * 0.2, arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2))
    ax.text(*(c + u * 1.05), name, color=color, fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85), zorder=5)
ax.set_aspect("equal")
ax.set_xlim(-5, 6)
ax.set_ylim(-5, 5)
ax.legend(fontsize=9, loc="upper left", frameon=True, framealpha=0.9)
ax.set_title("두 방향 후보", fontsize=11)


def sep(w):
    pa, pb = A @ w, B @ w
    return (pb.mean() - pa.mean()) ** 2 / (pa.var() + pb.var()), pa, pb


for ax, w, title, color in [(axes[1], w_naive, "평균 차이 방향으로 투영", GRAY), (axes[2], w_fisher, "피셔 방향으로 투영", RED)]:
    J, pa, pb = sep(w / np.linalg.norm(w))
    bins = np.linspace(min(pa.min(), pb.min()), max(pa.max(), pb.max()), 40)
    ax.hist(pa, bins=bins, color=BLUE, alpha=0.6)
    ax.hist(pb, bins=bins, color=ORANGE, alpha=0.6)
    ax.set_title(f"{title}\n분리도 J = {J:.2f}", fontsize=11, color=color if color == RED else "#222")
    ax.set_yticks([])
fig.tight_layout()
save(fig, "lda", "fisher-direction.png")

# ── 데이터 누수 그림 1. 구간 단위로 섞어 나누기 대 시행 단위로 나누기
fig, axes = plt.subplots(2, 1, figsize=(10, 3.6))
n_trials_v, bins_per = 8, 12
rng2 = np.random.default_rng(7)
for ax, title, mode in [(axes[0], "구간 단위로 무작위 분할: 같은 시행의 앞뒤가 학습과 시험에 나뉜다", "bin"),
                        (axes[1], "시행 단위로 분할: 한 시행은 통째로 한쪽에만 간다", "trial")]:
    test_trials = {2, 5}
    for tr in range(n_trials_v):
        for b in range(bins_per):
            x = tr * (bins_per + 2) + b
            if mode == "bin":
                is_test = rng2.random() < 0.25
            else:
                is_test = tr in test_trials
            ax.add_patch(plt.Rectangle((x, 0), 1, 1, fc=ORANGE if is_test else BLUE, ec="white", lw=0.8))
        ax.text(tr * (bins_per + 2) + bins_per / 2, 1.25, f"시행 {tr + 1}", ha="center", fontsize=9, color=GRAY)
    ax.set_xlim(-1, n_trials_v * (bins_per + 2))
    ax.set_ylim(-0.2, 1.7)
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=11)
axes[1].add_patch(plt.Rectangle((0, -0.15), 0.01, 0.01, fc=BLUE, label="학습"))
axes[1].add_patch(plt.Rectangle((0, -0.15), 0.01, 0.01, fc=ORANGE, label="시험"))
axes[1].legend(loc="lower right", fontsize=9.5, ncol=2, bbox_to_anchor=(1.0, -0.35))
fig.tight_layout()
save(fig, "data-leakage", "split-unit.png")

# ── 데이터 누수 그림 2. 사람마다 고유한 '지문'이 있는 자료: 분할 방식에 따라 정확도가 달라 보인다
n_subj, per_subj, dim = 40, 20, 12
subj_label = np.array([0] * 20 + [1] * 20)  # 사람 단위 라벨 (예: 환자/대조군)


def make_dataset():
    """사람마다 고유한 패턴(지문)이 있고, 집단 차이는 아주 작은 자료를 새로 만든다."""
    finger = rng.normal(0, 1.5, (n_subj, dim))  # 라벨과 무관한 사람별 패턴
    effect = np.zeros(dim)
    effect[0] = 0.25  # 진짜 집단 차이
    X = np.vstack([finger[s] + subj_label[s] * effect + rng.normal(0, 1.0, (per_subj, dim)) for s in range(n_subj)])
    y = np.repeat(subj_label, per_subj)
    g = np.repeat(np.arange(n_subj), per_subj)
    return X, y, g


def knn_acc(X, y, train, test):
    """1-최근접 이웃 분류기: 사람 지문을 외우기 가장 쉬운 분류기."""
    d = ((X[test][:, None, :] - X[train][None, :, :]) ** 2).sum(-1)
    return np.mean(y[train][np.argmin(d, axis=1)] == y[test])


def cv_random(X, y, g):
    idx = rng.permutation(len(y))
    return np.mean([knn_acc(X, y, np.setdiff1d(idx, f), f) for f in np.array_split(idx, 5)])


def cv_subject(X, y, g):
    # 층화: 폴드마다 두 집단을 같은 수만큼 넣어 학습 세트의 집단 비율이 기울지 않게 한다
    s0 = rng.permutation(np.where(subj_label == 0)[0])
    s1 = rng.permutation(np.where(subj_label == 1)[0])
    sfolds = [np.r_[a, b] for a, b in zip(np.array_split(s0, 5), np.array_split(s1, 5))]
    return np.mean([knn_acc(X, y, np.where(~np.isin(g, sf))[0], np.where(np.isin(g, sf))[0]) for sf in sfolds])


# 자료를 40번 새로 만들어 평균한다. 자료 한 벌의 결과는 그 사람들의 우연한 배치에 크게 흔들린다
accs = np.array([[cv_random(*d), cv_subject(*d)] for d in (make_dataset() for _ in range(40))])
acc_random, acc_subj = accs.mean(axis=0)
fig, ax = plt.subplots(figsize=(7.5, 3.0))
ax.barh(["표본 단위 무작위 5겹", "사람 단위 5겹 (층화)"], [acc_random, acc_subj], color=[RED, BLUE], height=0.5)
ax.axvline(0.5, color=GRAY, ls="--")
ax.text(0.505, 1.33, "우연 수준 50%", color=GRAY, fontsize=9.5)
for i, v in enumerate([acc_random, acc_subj]):
    ax.text(v + 0.01, i, f"{v:.0%}", va="center", fontsize=11, fontweight="bold")
ax.set_xlim(0, 1.08)
ax.invert_yaxis()
ax.set_xlabel("정확도")
ax.set_title("같은 자료, 같은 분류기. 나누는 단위만 다르다 (합성 자료 40벌 평균)", loc="left", fontsize=11)
save(fig, "data-leakage", "subject-split.png")
print("acc random", acc_random, "acc subject", acc_subj, "csp lam", lam[[0, -1]])
