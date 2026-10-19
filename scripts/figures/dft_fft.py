"""DFT와 FFT 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, pi_ticks, save, setup

ARTICLE = "dft-fft"
setup()


def dtft(x, w):
    n = np.arange(len(x))
    return np.array([np.sum(x * np.exp(-1j * wi * n)) for wi in w])


# 그림 1. DFT는 DTFT 위의 점이다 (0을 덧붙이면 같은 곡선 위의 점이 촘촘해질 뿐)
x = np.array([1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0])
w = np.linspace(0, 2 * np.pi, 2000)
fig, ax = plt.subplots(figsize=(8.5, 3.4))
ax.plot(w, np.abs(dtft(x, w)), color=GRAY, lw=1.6, label="DTFT 크기 (연속 곡선)")
for N, color, marker, label in [(32, TEAL, "o", "32점 DFT (0을 덧붙임)"), (8, RED, "s", "8점 DFT")]:
    xk = np.abs(np.fft.fft(x, N))
    wk = 2 * np.pi * np.arange(N) / N
    ax.plot(wk, xk, marker, color=color, ms=6 if N == 8 else 4, label=label, zorder=4 if N == 8 else 3)
pi_ticks(ax, 0, 2, 0.5)
ax.set_xlabel("ω (rad/표본)")
ax.set_ylabel("크기")
ax.set_title("DFT는 DTFT 곡선을 N개 지점에서 뽑은 값이다")
ax.legend(loc="upper center", ncol=3, fontsize=9.5)
ax.set_ylim(0, 5)
save(fig, ARTICLE, "dft-samples-dtft.png")

# 그림 2. 누설: 주파수가 칸에 딱 맞으면 한 칸, 어긋나면 번진다. 창 함수로 줄인다
N = 64
n = np.arange(N)
k = np.arange(N // 2)
fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
cases = [
    (8.0, None, "칸에 딱 맞음 (8칸)"),
    (8.5, None, "칸 사이 (8.5칸)"),
    (8.5, np.hanning(N), "칸 사이 + Hann 창"),
]
for ax, (f, win, title) in zip(axes, cases):
    s = np.cos(2 * np.pi * f * n / N)
    if win is not None:
        s = s * win / np.mean(win)
    X = np.abs(np.fft.fft(s))[: N // 2] / (N / 2)
    db = 20 * np.log10(np.maximum(X, 1e-6))
    ax.vlines(k, -80, db, color=RED if win is None and f % 1 else BLUE, lw=1.4)
    ax.plot(k, db, "o", ms=3, color=RED if win is None and f % 1 else BLUE)
    ax.set_title(title)
    ax.set_xlabel("주파수 칸 k")
    ax.set_xlim(0, 31)
    ax.set_ylim(-80, 5)
axes[0].set_ylabel("크기 (dB)")
fig.tight_layout()
save(fig, ARTICLE, "leakage.png")

# 그림 3. 0을 덧붙여도 가까운 두 주파수는 갈라지지 않는다. 더 오래 재야 갈라진다
fs = 100.0
f1, f2 = 20.0, 21.0


def spectrum(T, nfft):
    t = np.arange(int(T * fs)) / fs
    s = np.cos(2 * np.pi * f1 * t) + np.cos(2 * np.pi * f2 * t)
    S = np.abs(np.fft.rfft(s * np.hanning(len(s)), nfft))
    f = np.fft.rfftfreq(nfft, 1 / fs)
    return f, S / S.max()


fig, axes = plt.subplots(1, 3, figsize=(10, 3.1), sharey=True)
for ax, (T, nfft, title) in zip(
    axes,
    [(0.5, 50, "0.5초 기록"), (0.5, 4096, "0.5초 기록 + 0 덧붙임"), (4.0, 4096, "4초 기록")],
):
    f, S = spectrum(T, nfft)
    ax.plot(f, S, color=BLUE, lw=1.6, marker="o" if nfft < 100 else None, ms=3)
    for fc in (f1, f2):
        ax.axvline(fc, color=ORANGE, ls=":", lw=1)
    ax.set_xlim(10, 31)
    ax.set_title(title)
    ax.set_xlabel("주파수 (Hz)")
axes[0].set_ylabel("정규화한 크기")
fig.suptitle("20 Hz와 21 Hz (fs = 100 Hz, Hann 창): 해상도는 기록 길이가 정한다", fontweight="bold", y=1.02)
fig.tight_layout()
save(fig, ARTICLE, "resolution.png")

# 그림 4. 8점 FFT의 나비 구조 (시간 솎음, radix-2)
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.axis("off")
xs = [0, 2.2, 4.4, 6.6]
order = [0, 4, 2, 6, 1, 5, 3, 7]
ys = np.arange(8)[::-1] * 0.7
for i, y in enumerate(ys):
    ax.text(xs[0] - 0.15, y, f"x[{order[i]}]", ha="right", va="center", fontsize=11)
    ax.text(xs[-1] + 0.15, y, f"X[{i}]", ha="left", va="center", fontsize=11)
    for x in xs:
        ax.plot(x, y, "o", color=BLUE, ms=5, zorder=3)
stage_pairs = [
    [(0, 1), (2, 3), (4, 5), (6, 7)],
    [(0, 2), (1, 3), (4, 6), (5, 7)],
    [(0, 4), (1, 5), (2, 6), (3, 7)],
]
colors = [TEAL, ORANGE, RED]
for s, pairs in enumerate(stage_pairs):
    x0, x1 = xs[s], xs[s + 1]
    for a, b in pairs:
        ya, yb = ys[a], ys[b]
        for (p, q) in [(ya, ya), (yb, yb), (ya, yb), (yb, ya)]:
            ax.plot([x0, x1], [p, q], color=colors[s], lw=1.2, alpha=0.85)
for s, label in enumerate(["1단: 2점 DFT 4개", "2단: 4점 DFT 2개", "3단: 8점 DFT 1개"]):
    ax.text((xs[s] + xs[s + 1]) / 2, ys[0] + 0.55, label, ha="center", color=colors[s], fontsize=11, fontweight="bold")
ax.text((xs[0] + xs[-1]) / 2, ys[-1] - 0.75, "단마다 곱셈 N/2번 × log₂N단 = (N/2)·log₂N번  (N = 8이면 12번, 직접 계산은 64번)",
        ha="center", color=GRAY, fontsize=10.5)
ax.set_xlim(-1.2, 7.8)
ax.set_ylim(ys[-1] - 1.0, ys[0] + 0.9)
save(fig, ARTICLE, "butterfly.png")

# 그림 5. 계산량: N² 대 N log N
Ns = 2 ** np.arange(3, 17)
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.loglog(Ns, Ns.astype(float) ** 2, "o-", color=RED, label="직접 계산 (N²)")
ax.loglog(Ns, Ns / 2 * np.log2(Ns), "o-", color=BLUE, label="FFT ((N/2)·log₂N)")
ax.set_xlabel("N (점의 수)")
ax.set_ylabel("복소수 곱셈 횟수")
ax.set_title("N = 1024이면 약 100만 번 대 약 5천 번")
ax.legend()
save(fig, ARTICLE, "complexity.png")
