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

# VAE 증강 실험의 설계: 세 조건이 같은 디코더로 들어간다
fig, ax = plt.subplots(figsize=(11, 4.6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 4.6)
ax.axis("off")
box(ax, 0.1, 3.3, 2.3, 1.0, "전체 496시행")
box(ax, 0.1, 1.9, 2.3, 1.0, "100시행만")
box(ax, 2.7, 0.25, 2.0, 1.0, "VAE 학습\n(100시행으로)", "#eef4f2", TEAL)
box(ax, 5.0, 0.25, 2.0, 1.0, "생성 시행\n100 / 300 / 900개", "#eef4f2", TEAL)
box(ax, 7.3, 0.25, 1.8, 1.0, "100 실제\n+ 생성", "#fbeee0", ORANGE)
box(ax, 9.4, 0.25, 1.5, 4.05, "같은 MLP\n디코더\n\n시행 단위\n교차검증으로\n비교", LIGHT, RED)
arrow(ax, 2.4, 3.8, 9.4, 3.8)
arrow(ax, 2.4, 2.4, 9.4, 2.4)
arrow(ax, 1.25, 1.9, 2.7, 0.75)
arrow(ax, 4.7, 0.75, 5.0, 0.75)
arrow(ax, 7.0, 0.75, 7.3, 0.75)
arrow(ax, 9.1, 0.75, 9.4, 0.75)
ax.text(5.9, 3.95, "조건 1: 전체 자료 (성능 상한)", ha="center", color=GRAY, fontsize=9.5)
ax.text(5.9, 2.55, "조건 2: 적은 자료만 (기준선)", ha="center", color=GRAY, fontsize=9.5)
ax.text(8.2, 1.4, "조건 3: 적은 자료 + 증강", ha="center", color=ORANGE, fontsize=9.5)
save(fig, "project-vae", "design.png")
