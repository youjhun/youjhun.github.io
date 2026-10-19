"""논문 리뷰(ASBIT 무선 센서 네트워크)의 그림. 논문 그림을 옮기지 않고 직접 그린 도식이다."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "paper-asbit"
setup()


def box(ax, x, y, w, h, text, fc, ec, color="#222"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10.5, color=color)


def arrow(ax, x0, y0, x1, y1, color=GRAY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))


# 그림 1. 전체 흐름
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.6)
ax.axis("off")
ax.text(0.05, 4.35, "센서 쪽 (칩마다 따로, 서로 시계를 맞추지 않는다)", color=BLUE, fontsize=11, fontweight="bold")
ax.text(0.05, 1.95, "수신기 쪽 (한 곳에서 전부 받는다)", color=TEAL, fontsize=11, fontweight="bold")
w, h = 2.1, 1.1
top = [
    ("사건 감지\n문턱을 넘으면 1비트", 0.1),
    ("고유 Gold code로\n부호화", 2.6),
    ("후방산란으로 송신\n(사건이 있을 때만)", 5.1),
    ("칩들이 되쏜 신호가\n수신 코일에서 더해진다", 7.6),
]
for text, x in top:
    box(ax, x, 2.95, w, h, text, LIGHT, BLUE)
for (_, x0), (_, x1) in zip(top, top[1:]):
    arrow(ax, x0 + w, 3.5, x1, 3.5)
bottom = [
    ("SNN 디코더\n→ 커서 속도", 0.1),
    ("노드별 사건 복원\n(문턱값 비교)", 2.6),
    ("정합 필터 묶음\n(노드마다 한 벌)", 5.1),
    ("겹친 RF 신호\n(I/Q로 받음)", 7.6),
]
for text, x in bottom:
    box(ax, x, 0.55, w, h, text, "#eef4f2", TEAL)
for (_, x0), (_, x1) in zip(bottom[1:], bottom[:-1]):
    arrow(ax, x0, 1.1, x1 + w, 1.1)
arrow(ax, 7.6 + w / 2, 2.95, 7.6 + w / 2, 1.65, color=ORANGE)
ax.text(7.6 + w / 2 + 0.1, 2.3, "무선 링크", color=ORANGE, fontsize=10)
save(fig, ARTICLE, "pipeline.png")

# 그림 2. 자원을 쓰는 방식: 고정 슬롯 vs 사건 기반
rng = np.random.default_rng(4)
nodes = 4
frames = 12
fig, axes = plt.subplots(2, 1, figsize=(9, 4.4), sharex=True)
# 사건 시각(연속)을 먼저 정하고, 두 방식이 같은 사건을 어떻게 보내는지 그린다
events = [np.sort(rng.uniform(0.5, frames - 1.5, size=k)) for k in (2, 1, 3, 1)]
ax = axes[0]
for i in range(nodes):
    # 노드 i의 칸은 매 프레임 f + i/nodes에 온다. 사건은 그 시각 이후 첫 칸에서 보고된다
    slots = np.arange(frames) + i / nodes
    reported = {int(np.argmax(slots >= t)) for t in events[i]}
    for f, start in enumerate(slots):
        ax.add_patch(plt.Rectangle((start, i), 1 / nodes, 0.8, fc=RED if f in reported else "#d9d9d9", ec="white"))
    ax.plot(events[i], [i + 0.95] * len(events[i]), "v", color=ORANGE, ms=6)
ax.set_title("고정 시간 슬롯: 사건이 없어도 매 프레임 자기 칸을 쓴다 (회색 = 빈 전송, ▼ = 사건 발생)", loc="left")
ax = axes[1]
for i in range(nodes):
    for t in events[i]:
        ax.add_patch(plt.Rectangle((t, i), 0.45, 0.8, fc=RED, ec="white"))
    ax.plot(events[i], [i + 0.95] * len(events[i]), "v", color=ORANGE, ms=6)
ax.set_title("ASBIT: 사건이 생긴 노드만 그때 보낸다. 겹치면 부호로 가른다", loc="left")
for ax in axes:
    ax.set_ylim(-0.2, nodes + 0.2)
    ax.set_yticks(np.arange(nodes) + 0.4)
    ax.set_yticklabels([f"노드 {i + 1}" for i in range(nodes)])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
axes[1].set_xlim(0, frames)
axes[1].set_xlabel("시간 (프레임)")
fig.tight_layout()
save(fig, ARTICLE, "resource.png")

# 그림 3. 논문이 보고한 수용 노드 수 (평균 사건율 50 Hz, SNR 1.7 dB)
fig, ax = plt.subplots(figsize=(8, 2.6))
labels = ["칩 안의 자유 발진기\n(EER 1.19×10⁻³)", "RF 반송파 분주 클록\n(EER 1.03×10⁻³)"]
vals = [750, 2500]
ax.barh(labels, vals, color=[BLUE, TEAL], height=0.55)
for y, v in enumerate(vals):
    ax.text(v + 40, y, f"{v:,}개", va="center", fontsize=11, fontweight="bold")
ax.set_xlim(0, 2900)
ax.set_xlabel("오류율 약 10⁻³에서 수용한 노드 수")
ax.set_title("클록을 어디서 얻느냐에 따라 수용 규모가 3배 넘게 달라졌다", loc="left")
ax.invert_yaxis()
ax.grid(axis="y", visible=False)
save(fig, ARTICLE, "capacity.png")
