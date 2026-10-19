"""샘플링과 앨리어싱 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "sampling-aliasing"
setup()

# 그림 1. 연속 신호와 표본
t = np.linspace(0, 1, 2000)
fs = 20
n = np.arange(0, fs + 1)
fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(t, np.sin(2 * np.pi * 2 * t), color=GRAY, lw=1.6, label="연속 신호 x(t) (2 Hz)")
ax.vlines(n / fs, 0, np.sin(2 * np.pi * 2 * n / fs), color=BLUE, lw=1.2)
ax.plot(n / fs, np.sin(2 * np.pi * 2 * n / fs), "o", color=BLUE, ms=5, label="표본 x[n] = x(nT), T = 1/20 s")
ax.axhline(0, color="#555", lw=0.8)
ax.set_xlabel("시간 (s)")
ax.set_ylabel("진폭")
ax.set_title("연속 신호를 T초마다 재면 점의 열이 남는다")
ax.legend(loc="upper right", ncol=2, fontsize=9.5)
ax.set_ylim(-1.35, 1.6)
save(fig, ARTICLE, "sampling.png")

# 그림 2. 시간 영역의 앨리어싱: 9 Hz를 10 Hz로 재면 1 Hz처럼 보인다
fs = 10
n = np.arange(0, fs + 1)
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.plot(t, np.cos(2 * np.pi * 9 * t), color=GRAY, lw=0.9, label="실제 신호 (9 Hz)")
ax.plot(t, np.cos(2 * np.pi * 1 * t), "--", color=ORANGE, lw=2, label="표본이 보여 주는 신호 (1 Hz)")
ax.plot(n / fs, np.cos(2 * np.pi * 9 * n / fs), "o", color=RED, ms=7, zorder=5, label="표본 (fs = 10 Hz)")
ax.set_xlabel("시간 (s)")
ax.set_ylabel("진폭")
ax.set_title("9 Hz 코사인을 초당 10번 재면 1 Hz 코사인과 같은 점이 찍힌다")
ax.legend(loc="lower center", ncol=3, fontsize=9.5, bbox_to_anchor=(0.5, -0.45))
save(fig, ARTICLE, "aliasing-time.png")


# 그림 3. 주파수 영역: 스펙트럼 복사본이 fs 간격으로 반복되고, 대역이 넓으면 겹친다
def tri(f, b):
    return np.clip(1 - np.abs(f) / b, 0, None)


f = np.linspace(-2.45, 2.45, 4000)  # fs = 1로 정규화
fig, axes = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
for ax, b, title in [
    (axes[0], 0.4, "대역폭 B가 fs/2보다 작으면 복사본이 겹치지 않는다"),
    (axes[1], 0.75, "대역폭 B가 fs/2보다 크면 복사본이 겹친다 (앨리어싱)"),
]:
    total = np.zeros_like(f)
    for k in range(-3, 4):
        c = tri(f - k, b)
        total += c
        ax.plot(f, c, color=BLUE if k == 0 else TEAL, lw=1.6 if k == 0 else 1.1, alpha=1 if k == 0 else 0.8)
    ax.fill_between(f, 0, tri(f, b), color=LIGHT, zorder=0)
    if b > 0.5:
        overlap = np.minimum(tri(f, b), tri(f - 1, b)) + np.minimum(tri(f, b), tri(f + 1, b))
        ax.fill_between(f, 0, overlap, color=RED, alpha=0.35, label="겹친 부분")
        ax.plot(f, total, color=RED, lw=1.2, ls=":", label="실제로 남는 합")
        ax.legend(loc="upper right", fontsize=9.5)
    for x in (-0.5, 0.5):
        ax.axvline(x, color=ORANGE, lw=1.2, ls="--")
    ax.set_title(title)
    ax.set_ylim(0, 1.25)
    ax.set_yticks([])
axes[0].text(0.53, 1.12, "fs/2", color=ORANGE, ha="left")
axes[0].text(-0.53, 1.12, "−fs/2", color=ORANGE, ha="right")
axes[1].set_xticks([-2, -1, 0, 1, 2])
axes[1].set_xticklabels(["−2fs", "−fs", "0", "fs", "2fs"])
axes[1].set_xlabel("주파수")
fig.tight_layout()
save(fig, ARTICLE, "aliasing-spectrum.png")

# 그림 4. 접힘: 실제 주파수 → 표본에서 보이는 주파수 (fs = 200 Hz)
fs = 200
F = np.linspace(0, 800, 4000)
apparent = np.abs(F - fs * np.round(F / fs))
fig, ax = plt.subplots(figsize=(8, 3.3))
ax.plot(F, apparent, color=BLUE, lw=2)
for k in range(1, 8):
    ax.axvline(k * fs / 2, color=GRAY, lw=0.7, ls=":")
ax.axhline(fs / 2, color=ORANGE, lw=1.2, ls="--")
ax.text(805, fs / 2, "fs/2 = 100 Hz", color=ORANGE, va="center")
ax.plot([360], [40], "o", color=RED, ms=8, zorder=5)
ax.annotate("360 Hz는 40 Hz로 보인다", (360, 40), (395, 72), color=RED,
            arrowprops=dict(arrowstyle="->", color=RED),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=RED, lw=0.8), zorder=6)
ax.set_xlabel("실제 주파수 F (Hz)")
ax.set_ylabel("보이는 주파수 (Hz)")
ax.set_title("fs = 200 Hz로 재면 모든 주파수가 0~100 Hz 안으로 접힌다")
ax.set_xlim(0, 800)
ax.set_ylim(0, 115)
save(fig, ARTICLE, "folding.png")
