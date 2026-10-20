"""프로젝트 페이지의 흐름도."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

setup()


def box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def arrow(ax, x0, y0, x1, y1, color=GRAY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))


# 조현병 EEG 분류 실습의 흐름
fig, ax = plt.subplots(figsize=(11, 3.2))
ax.set_xlim(0, 11)
ax.set_ylim(0, 3.2)
ax.axis("off")
steps = [
    ("EDF 원자료\n(사람마다 한 파일)", LIGHT, BLUE),
    ("대역 필터\n+ 구간 나누기", LIGHT, BLUE),
    ("구간 × 채널마다\n통계 특징 12개", LIGHT, BLUE),
    ("로지스틱 회귀\n(규제 세기 C 탐색)", LIGHT, BLUE),
    ("사람 단위 교차검증\n(GroupKFold)", "#fbeee0", ORANGE),
]
w, h, gap = 1.85, 1.2, 0.33
for i, (t, fc, ec) in enumerate(steps):
    x = 0.1 + i * (w + gap)
    box(ax, x, 1.2, w, h, t, fc, ec)
    if i:
        arrow(ax, x - gap, 1.8, x, 1.8)
ax.text(0.1 + 4 * (w + gap) + w / 2, 0.75, "한 사람의 구간들은\n학습이든 시험이든 한쪽에만", ha="center", va="top", color=ORANGE, fontsize=9.5)
ax.text(0.1 + 2 * (w + gap) + w / 2, 0.75, "평균·표준편차·첨도 등\n(구간 수, 채널 수 × 12)", ha="center", va="top", color=GRAY, fontsize=9.5)
save(fig, "project-scz", "pipeline.png")
