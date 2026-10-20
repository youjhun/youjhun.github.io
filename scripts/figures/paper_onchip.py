"""논문 리뷰(퓨즈로 칩 하드웨어를 고치는 방법, Advanced Science 2023)의 그림. 논문 그림을 옮기지 않고 직접 그렸다."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "paper-onchip"
setup()


# 그림 1. 퓨즈와 안티퓨즈: 레이저로 끊고, 집속 이온빔(FIB)으로 백금을 올려 잇는다
def node(ax, x, y):
    ax.add_patch(Rectangle((x - 0.18, y - 0.18), 0.36, 0.36, fc="#cfd8de", ec=BLUE, lw=1.2))


fig, ax = plt.subplots(figsize=(10, 3.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.4)
ax.axis("off")
cols = [
    (1.1, "퓨즈 (만든 그대로)", "연결", BLUE, "line"),
    (3.7, "레이저로 끊음", "끊김", RED, "cut"),
    (6.3, "FIB로 백금을 올림", "다시 연결 (약 850 Ω)", TEAL, "pt"),
    (8.9, "안티퓨즈 (만든 그대로)", "끊김 → FIB로 연결", ORANGE, "gap"),
]
for x, title, state, color, kind in cols:
    y = 1.7
    node(ax, x - 0.7, y)
    node(ax, x + 0.7, y)
    if kind == "line":
        ax.plot([x - 0.52, x + 0.52], [y, y], color=BLUE, lw=5, solid_capstyle="butt")
    elif kind == "cut":
        ax.plot([x - 0.52, x - 0.12], [y, y], color=BLUE, lw=5, solid_capstyle="butt")
        ax.plot([x + 0.12, x + 0.52], [y, y], color=BLUE, lw=5, solid_capstyle="butt")
        ax.annotate("", xy=(x, y + 0.12), xytext=(x, y + 0.85), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
        ax.text(x, y + 0.9, "532 nm 레이저", ha="center", va="bottom", color=RED, fontsize=9.5)
    elif kind == "pt":
        ax.plot([x - 0.52, x - 0.12], [y, y], color=BLUE, lw=5, solid_capstyle="butt")
        ax.plot([x + 0.12, x + 0.52], [y, y], color=BLUE, lw=5, solid_capstyle="butt")
        ax.plot([x - 0.25, x + 0.25], [y + 0.07, y + 0.07], color=TEAL, lw=4, solid_capstyle="butt")
        ax.text(x, y + 0.9, "백금 200 nm", ha="center", va="bottom", color=TEAL, fontsize=9.5)
    else:
        ax.text(x, y + 0.9, "두 끝만 열어 둔다", ha="center", va="bottom", color=ORANGE, fontsize=9.5)
    ax.text(x, 3.15, title, ha="center", fontsize=10.5, fontweight="bold", color="#222")
    ax.text(x, 0.95, state, ha="center", fontsize=10, color=color)
for x in (2.4, 5.0):
    ax.annotate("", xy=(x + 0.3, 1.7), xytext=(x - 0.3, 1.7), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.4))
ax.plot([7.6, 7.6], [0.5, 3.1], color="#ddd", lw=1)
ax.text(5.0, 0.25, "가장 위 금속층(알루미늄)에만 만들어 두면, 공장에서 받은 칩을 그 자리에서 고칠 수 있다", ha="center", color=GRAY, fontsize=9.5)
save(fig, ARTICLE, "fuse-states.png")

# 그림 2. 시뮬레이션과 측정이 크게 어긋난 저역 차단 주파수 (논문 본문의 수치)
fig, ax = plt.subplots(figsize=(8, 3.3))
rows = [
    ("1단 증폭기", 1.12, 8.0),
    ("2단 증폭기", 1.75, 20.0),
]
for y, (name, sim, meas) in enumerate(rows):
    ax.plot([sim, meas], [y, y], color="#ccc", lw=2, zorder=1)
    ax.plot(sim, y, "o", color=GRAY, ms=9, zorder=2, label="시뮬레이션" if y == 0 else None)
    ax.plot(meas, y, "o", color=RED, ms=9, zorder=2, label="측정" if y == 0 else None)
    ax.text(sim / 1.12, y - 0.32, f"{sim} Hz", ha="center", color=GRAY, fontsize=9.5)
    ax.text(meas * 1.05, y - 0.32, f"약 {meas:g} Hz", ha="center", color=RED, fontsize=9.5)
    ax.text(np.sqrt(sim * meas), y + 0.12, f"{meas / sim:.0f}배", ha="center", va="top", color="#555", fontsize=9.5)
for y, (name, f) in enumerate([("의사저항 a", 2.5), ("의사저항 b", 3.5), ("의사저항 c", 4.5)], start=2):
    ax.plot(f, y, "o", color=RED, ms=9)
    ax.text(f * 1.12, y, f"약 {f} Hz", va="center", color=RED, fontsize=9.5)
ax.set_xscale("log")
ax.set_xlim(0.7, 40)
ax.set_xticks([1, 2, 5, 10, 20])
ax.set_xticklabels(["1", "2", "5", "10", "20"])
ax.set_yticks(range(5))
ax.set_yticklabels(["1단 증폭기", "2단 증폭기", "1단 + 의사저항 a", "1단 + 의사저항 b", "1단 + 의사저항 c"])
ax.set_ylim(-0.7, 4.5)
ax.invert_yaxis()
ax.set_xlabel("저역 차단 주파수 (Hz, 로그 눈금)")
ax.set_title("의사저항은 시뮬레이션대로 나오지 않는다", loc="left")
ax.legend(loc="lower right", fontsize=9.5, frameon=True, framealpha=0.95, edgecolor="#ddd")
ax.grid(axis="y", visible=False)
save(fig, ARTICLE, "cutoff.png")

# 그림 3. 공진 커패시터를 퓨즈로 하나씩 떼어 낸다 (전체 값은 논문의 범례, 계산은 직접)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axes[0]
total = 2.34
steps = [
    ("처음 (전부 연결)", total, []),
    ("340 fF를 끊음", total - 0.340, ["340"]),
    ("512 fF를 끊음", total - 0.512, ["512"]),
    ("둘 다 끊음", total - 0.340 - 0.512, ["340", "512"]),
]
for i, (name, c, cut) in enumerate(steps):
    ax.barh(i, c, color=BLUE if not cut else TEAL, height=0.55)
    ax.text(c + 0.03, i, f"{c:.2f} pF", va="center", fontsize=10, fontweight="bold")
ax.set_yticks(range(4))
ax.set_yticklabels([s[0] for s in steps])
ax.invert_yaxis()
ax.set_xlim(0, 2.8)
ax.set_xlabel("칩 코일에 병렬로 걸린 전체 커패시턴스 (pF)")
ax.set_title("2.34 − 0.34 = 2.00, 2.34 − 0.512 ≈ 1.83, 둘 다 빼면 ≈ 1.49", loc="left", fontsize=11)
ax.grid(axis="y", visible=False)
ax = axes[1]
labels = ["공기", "머리 팬텀\n(액체)"]
before, after = [6, 10], [6, 10 - 1.33]
x = np.arange(2)
ax.bar(x - 0.18, before, width=0.34, color=BLUE, label="2.34 pF")
ax.bar(x + 0.18, after, width=0.34, color=TEAL, label="2.00 pF (340 fF 끊음)")
for xi, b, a in zip(x, before, after):
    ax.text(xi - 0.18, b + 0.25, f"{b:g}", ha="center", fontsize=10)
    ax.text(xi + 0.18, a + 0.25, f"{a:g}", ha="center", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(0, 12.5)
ax.set_ylabel("칩을 켜는 데 필요한 송신 전력 (dBm)")
ax.set_title("915 MHz에서 팬텀 쪽만 1.33 dB 낮아졌다", loc="left", fontsize=11)
ax.legend(loc="upper left", fontsize=9.5)
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, ARTICLE, "cap-tuning.png")
