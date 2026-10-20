"""논문 리뷰(무선 미세 자극기 네트워크로 패턴 전기 자극, Nature Communications 2024)의 그림. 논문 그림을 옮기지 않고 직접 그렸다."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "paper-stim"
setup()

# 그림 1. 데이지 체인 하향 명령: sync 뒤에 칩마다 3비트씩 이어 붙인다. 주소가 N인 칩은 N번째 3비트를 읽는다
fig, ax = plt.subplots(figsize=(10, 3.0))
ax.set_xlim(-0.2, 13.5)
ax.set_ylim(-1.6, 2.2)
ax.axis("off")
ax.add_patch(plt.Rectangle((0, 0.6), 2.2, 0.9, fc="#d9d9d9", ec="white"))
ax.text(1.1, 1.05, "sync", ha="center", va="center", fontsize=11)
cmds = ["011", "000", "110", "011", "101", "001"]
for i, c in enumerate(cmds):
    x = 2.2 + i * 1.6
    ax.add_patch(plt.Rectangle((x, 0.6), 1.6, 0.9, fc=LIGHT if i != 2 else "#f6e3c8", ec="white", lw=2))
    ax.text(x + 0.8, 1.05, c, ha="center", va="center", fontsize=11, family="monospace")
    ax.text(x + 0.8, 1.75, f"{i + 1}번 칩", ha="center", fontsize=9.5, color=GRAY)
ax.text(2.2 + 6 * 1.6 + 0.3, 1.05, "…", fontsize=14, va="center")
ax.annotate("", xy=(2.2 + 2 * 1.6 + 0.8, 0.55), xytext=(2.2 + 2 * 1.6 + 0.8, -0.35), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
ax.text(2.2 + 2 * 1.6 + 0.8, -0.75, "주소가 3인 칩은 세 번째 3비트만 읽고\n그 값에 맞는 파형으로 자극한다", ha="center", va="top", color=ORANGE, fontsize=9.5)
ax.text(0, -0.75, "칩 하나에 3비트 = 1 Mbps에서 3 µs", color=BLUE, fontsize=10, va="top")
ax.text(13.4, -0.75, "칩 1,000개면 3 ms\n(sync 길이는 뺀 값)", color=BLUE, fontsize=10, va="top", ha="right")
save(fig, ARTICLE, "daisy-chain.png")

# 그림 2. 칩 N개에 명령을 돌리는 시간: 데이지 체인 대 2021년의 호출-응답 (두 논문의 수치로 직접 계산)
N = np.logspace(0, 3.3, 200)
daisy = N * 3e-6
call = N * (0.1 / 425)  # 2021년 논문: 100 ms 안에 칩 425개와 주고받았다
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.loglog(N, daisy * 1e3, color=TEAL, lw=2.2, label="데이지 체인 (2024): 칩마다 3 µs")
ax.loglog(N, call * 1e3, color=GRAY, lw=2, ls="--", label="호출-응답 (2021): 100 ms에 425개, 칩마다 약 235 µs")
for n, label in [(30, "만성 실험 30개"), (1000, "1,000개")]:
    ax.axvline(n, color=ORANGE, ls=":", lw=1)
    ax.text(n * 1.08, 1.5e-3, label, color=ORANGE, fontsize=9.5, va="bottom")
ax.plot(1000, 3, "o", color=TEAL, ms=7)
ax.text(1000 / 1.15, 3, "3 ms", ha="right", va="bottom", color=TEAL, fontsize=10, fontweight="bold")
ax.set_xlabel("칩 수")
ax.set_ylabel("명령을 한 바퀴 돌리는 시간 (ms)")
ax.set_ylim(1e-3, 1e3)
ax.set_title("명령을 한 바퀴 돌리는 시간 (호출-응답은 응답 시간 포함)", loc="left")
ax.legend(loc="upper left", fontsize=9.5)
save(fig, ARTICLE, "latency.png")

# 그림 3. 레버 과제 정답률과 95% 신뢰구간 (시행 50회, 독립 가정, 정확 이항 구간으로 직접 계산)
conds = [
    ("30개 동시, 50 Hz", 0.96),
    ("2개 · 감각피질 (N2)", 0.86),
    ("2개 · 운동피질 (N′2)", 0.62),
    ("1개 · 50 Hz, 500 µs (RF 9.5%)", 0.90),
    ("1개 · 20 Hz, 100 µs (RF 1.4%)", 0.82),
]
n = 50
fig, ax = plt.subplots(figsize=(8.5, 3.6))
for i, (name, p) in enumerate(conds):
    k = round(p * n)
    lo = beta.ppf(0.025, k, n - k + 1)
    hi = beta.ppf(0.975, k + 1, n - k) if k < n else 1.0
    color = RED if lo <= 0.5 else BLUE
    ax.plot([lo * 100, hi * 100], [i, i], color=color, lw=3, solid_capstyle="round", alpha=0.45)
    ax.plot(p * 100, i, "o", color=color, ms=8)
    ax.text(hi * 100 + 1.2, i, f"{k}/50  [{lo * 100:.1f}–{hi * 100:.1f}%]", va="center", fontsize=9.5, color=color)
ax.axvline(50, color=GRAY, ls="--", lw=1.2)
ax.text(50.8, -0.55, "우연 (50%)", color=GRAY, fontsize=9.5, va="center")
ax.set_ylim(-0.8, 4.5)
ax.set_yticks(range(len(conds)))
ax.set_yticklabels([c[0] for c in conds])
ax.invert_yaxis()
ax.set_xlim(40, 112)
ax.set_xticks([40, 50, 60, 70, 80, 90, 100])
ax.set_xlabel("정답률 (%)")
ax.set_title("레버 과제 정답률과 정확 이항 95% 구간 (시행 50회)", loc="left")
ax.grid(axis="y", visible=False)
save(fig, ARTICLE, "behavior-ci.png")

# 그림 4. 듀티 사이클이 평균 RF 노출을 줄인다 (SAR, 10 g 평균, W/kg, 로그 눈금)
fig, ax = plt.subplots(figsize=(8, 3.2))
rows = [
    ("인체 조직 기준", 10, GRAY),
    ("낮은 단계 기준", 2, GRAY),
    ("100 mW를 계속 켰을 때 (시뮬레이션)", 1, BLUE),
    ("듀티 1.4%로 켰을 때", 0.0145, TEAL),
]
for i, (name, v, color) in enumerate(rows):
    ax.barh(i, v, color=color, height=0.55, alpha=0.6 if color == GRAY else 1)
    ax.text(v * 1.25, i, f"{v:g} W/kg", va="center", fontsize=10)
ax.set_xscale("log")
ax.set_xlim(5e-3, 60)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows])
ax.invert_yaxis()
ax.set_xlabel("최대 국소 SAR (W/kg, 로그 눈금)")
ax.set_title("최대 국소 SAR: 연속 송신과 듀티 1.4% 송신", loc="left")
ax.grid(axis="y", visible=False)
save(fig, ARTICLE, "sar.png")
