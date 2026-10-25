"""디지털 필터와 컨볼루션, 랜덤 신호와 자기상관, 전력 스펙트럼과 위너 필터 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, welch

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

# 컨볼루션 예: h[n] = a^n u[n], x[n] = u[n] − u[n−N]
ARTICLE = "digital-filters-convolution"
a, N = 0.9, 10
n = np.arange(-10, 41)
h = np.where(n >= 0, a ** np.clip(n, 0, None), 0.0)
x = ((n >= 0) & (n < N)).astype(float)
y = np.convolve(x[n >= 0], h[n >= 0])[: len(n[n >= 0])]
y = np.concatenate([np.zeros((n < 0).sum()), y])
fig, axes = plt.subplots(3, 1, figsize=(8.5, 5.6), sharex=True)
for ax, sig, color, title in [
    (axes[0], h, BLUE, "임펄스 응답 h[n] = 0.9ⁿ u[n]"),
    (axes[1], x, TEAL, "입력 x[n] = u[n] − u[n − 10]"),
    (axes[2], y, RED, "출력 y[n] = x[n] ∗ h[n]"),
]:
    ax.vlines(n, 0, sig, color=color, lw=1.4)
    ax.plot(n, sig, "o", color=color, ms=3.2)
    ax.set_title(title, loc="left")
axes[2].axhline(1 / (1 - a), color=GRAY, ls="--", lw=1)
axes[2].text(30, 1 / (1 - a) - 1.2, "1/(1 − a) = 10", color=GRAY, fontsize=9.5)
axes[2].set_xlabel("n")
fig.tight_layout()
save(fig, ARTICLE, "convolution-example.png")

# 자기상관: 1차 자기회귀 과정의 R_y[k]와 잡음 속 정현파
ARTICLE = "random-signals-autocorrelation"
rng = np.random.default_rng(582)
k = np.arange(-20, 21)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
for aa, color in [(0.0, GRAY), (0.5, TEAL), (0.9, BLUE)]:
    w = rng.standard_normal(400_000)
    yy = lfilter([1], [1, -aa], w)
    est = np.array([np.mean(yy[abs(kk):] * yy[: len(yy) - abs(kk)]) for kk in k])
    theory = aa ** np.abs(k) / (1 - aa**2)
    axes[0].plot(k, theory, color=color, lw=1.6, label=f"a = {aa}")
    axes[0].plot(k, est, "o", color=color, ms=3)
axes[0].set_title("y[n] = a·y[n−1] + w[n]의 자기상관", loc="left")
axes[0].set_xlabel("지연 k")
axes[0].set_ylabel("$R_y[k]$  ($\\sigma_w^2 = 1$)")
axes[0].legend(fontsize=9.5)

nn = np.arange(20_000)
s = np.cos(2 * np.pi * 0.05 * nn)
xn = s + 2.0 * rng.standard_normal(len(nn))
kk = np.arange(0, 61)
Rx = np.array([np.mean(xn[q:] * xn[: len(xn) - q]) for q in kk])
axes[1].plot(kk, Rx, color=RED, lw=1.6, marker="o", ms=3)
axes[1].plot(kk, 0.5 * np.cos(2 * np.pi * 0.05 * kk), color=GRAY, lw=1, ls="--", label="정현파만의 $R_s[k] = \\frac{1}{2}\\cos 2\\pi f k$")
axes[1].set_title("진폭 1 정현파 + 표준편차 2 백색잡음의 자기상관", loc="left")
axes[1].set_xlabel("지연 k")
axes[1].set_ylim(-0.8, 1.6)
axes[1].legend(fontsize=9, loc="upper right")
fig.tight_layout()
save(fig, ARTICLE, "autocorrelation.png")

# 잡음 속 정현파의 파형 (같은 신호의 앞부분)
fig, ax = plt.subplots(figsize=(10, 2.4))
ax.plot(nn[:200], xn[:200], color=GRAY, lw=1, label="관측 x[n]")
ax.plot(nn[:200], s[:200], color=RED, lw=1.6, label="숨은 정현파 (f = 0.05)")
ax.set_xlabel("n")
ax.set_title("표준편차 2인 백색잡음에 묻힌 진폭 1 정현파", loc="left")
ax.legend(fontsize=9, loc="upper right", ncol=2)
save(fig, ARTICLE, "sine-in-noise.png")

# 전력 스펙트럼: 1차 자기회귀 과정과 위너 필터
ARTICLE = "power-spectrum-wiener-filter"
f = np.linspace(0, 0.5, 501)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
for aa, color in [(0.5, TEAL), (0.9, BLUE)]:
    S = 1 / (1 - 2 * aa * np.cos(2 * np.pi * f) + aa**2)
    w = rng.standard_normal(400_000)
    yy = lfilter([1], [1, -aa], w)
    fw, Pw = welch(yy, fs=1.0, nperseg=1024, detrend=False, return_onesided=False)
    sel = (fw >= 0) & (fw <= 0.5)
    axes[0].semilogy(f, S, color=color, lw=2, label=f"이론값, a = {aa}")
    axes[0].semilogy(fw[sel], Pw[sel], color=color, lw=0.8, alpha=0.6)
axes[0].axhline(1, color=GRAY, ls="--", lw=1, label="백색잡음 ($\\sigma_w^2 = 1$)")
axes[0].set_title("1차 자기회귀 과정의 전력 스펙트럼", loc="left")
axes[0].set_xlabel("주파수 f (표본당 주기)")
axes[0].set_ylabel("$S_y(f)$")
axes[0].legend(fontsize=9)

aa, sw2 = 0.9, 10
Sy = 1 / (1 - 2 * aa * np.cos(2 * np.pi * f) + aa**2)
H = Sy / (Sy + sw2)
axes[1].semilogy(f, Sy, color=BLUE, lw=2, label="신호 $S_y(f)$, a = 0.9")
axes[1].semilogy(f, np.full_like(f, sw2), color=GRAY, lw=1.5, ls="--", label="잡음 $S_d(f) = 10$")
ax2 = axes[1].twinx()
ax2.plot(f, H, color=RED, lw=2, label="위너 필터 H(f)")
ax2.set_ylim(0, 1)
ax2.set_ylabel("H(f)", color=RED)
ax2.spines["right"].set_visible(True)
axes[1].set_title("신호·잡음 스펙트럼과 위너 필터", loc="left")
axes[1].set_xlabel("주파수 f (표본당 주기)")
l1, lab1 = axes[1].get_legend_handles_labels()
l2, lab2 = ax2.get_legend_handles_labels()
axes[1].legend(l1 + l2, lab1 + lab2, fontsize=9, loc="upper right")
fig.tight_layout()
save(fig, ARTICLE, "ar1-wiener.png")
