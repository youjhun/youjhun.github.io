"""논문 리뷰(뉴로그레인 무선 네트워크, Nature Electronics 2021)의 그림. 논문 그림을 옮기지 않고 직접 그렸다."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "paper-neurograins"
setup()


def box(ax, x, y, w, h, text, fc, ec, fontsize=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, color="#222")


def arrow(ax, x0, y0, x1, y1, color=GRAY, text=None, dy=0.12):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))
    if text:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + dy, text, ha="center", va="bottom", color=color, fontsize=9.5)


# 그림 1. 시스템 구성: 외부 허브 → 송신 코일 → 릴레이 코일 → 뉴로그레인
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.2)
ax.axis("off")
box(ax, 0.1, 1.5, 2.0, 1.2, "외부 허브\nSDR · 전력 증폭기\n· 듀플렉서", LIGHT, BLUE)
box(ax, 3.0, 1.5, 1.5, 1.2, "송신(Tx)\n코일", LIGHT, BLUE)
box(ax, 5.2, 1.5, 1.5, 1.2, "릴레이 코일\n(두피 아래)", LIGHT, BLUE)
box(ax, 7.5, 2.55, 2.4, 1.3, "기록용 뉴로그레인\n증폭기 → 8비트 ADC\n→ BPSK 후방산란", "#eef4f2", TEAL, 10)
box(ax, 7.5, 0.35, 2.4, 1.3, "자극용 뉴로그레인\nASK-PWM 해독 → 주소 확인\n→ 2상 전류 펄스", "#eef4f2", TEAL, 10)
arrow(ax, 2.1, 2.1, 3.0, 2.1)
arrow(ax, 4.5, 2.1, 5.2, 2.1, ORANGE)
ax.text(4.85, 2.85, "유도 결합", ha="center", color=ORANGE, fontsize=9.5)
arrow(ax, 6.7, 2.25, 7.5, 3.1, ORANGE)
arrow(ax, 6.7, 1.95, 7.5, 1.0, ORANGE)
ax.text(0.1, 3.75, "하향(전력 + 명령): 약 1 GHz 반송파, ASK-PWM 1 Mbps", color=BLUE, fontsize=10.5, fontweight="bold")
ax.text(0.1, 3.35, "상향(데이터): 약 30 MHz 부반송파에 실은 BPSK 후방산란 10 Mbps", color=TEAL, fontsize=10.5, fontweight="bold")
ax.text(0.1, 0.6, "칩 하나: 65 nm CMOS, 약 0.1 mm³, 외부 부품 없음\n칩마다 고유 주소(PUF 또는 레이저로 새긴 10비트)", color=GRAY, fontsize=9.5)
save(fig, ARTICLE, "system.png")

# 그림 2. 후방산란 스펙트럼: 반송파 옆 ±30 MHz에 10 Mbps BPSK 주엽을 둔다 (이상화)
f = np.linspace(-60, 60, 4001)
rb, fsub = 10.0, 30.0
lobe = lambda x: np.sinc((x) / rb) ** 2  # BPSK 전력 스펙트럼 모양, 첫 영점은 ±Rb
psd = 1e-3 * (lobe(f - fsub) + lobe(f + fsub))
fig, ax = plt.subplots(figsize=(8.5, 3.4))
ax.plot(f, 10 * np.log10(psd + 1e-9), color=TEAL, lw=1.6, label="상향 데이터 (BPSK, 10 Mbps)")
ax.vlines(0, -90, 0, color=BLUE, lw=3, label="전력 반송파 (Tx tone)")
for c in (-fsub, fsub):
    ax.axvspan(c - rb, c + rb, color=TEAL, alpha=0.08)
ax.annotate("주엽 폭 20 MHz\n(영점은 ±10 MHz)", xy=(fsub, -32), xytext=(43, -12), fontsize=9.5, color=TEAL,
            arrowprops=dict(arrowstyle="-", color=TEAL, lw=1))
ax.annotate("", xy=(fsub, -15), xytext=(0, -15), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax.text(fsub / 2, -13, "약 30 MHz", ha="center", va="bottom", color=GRAY, fontsize=9.5)
ax.set_xlim(-60, 60)
ax.set_ylim(-90, 5)
ax.set_xlabel("반송파에서 떨어진 주파수 (MHz)")
ax.set_ylabel("상대 전력 (dB)")
ax.set_title("데이터를 30 MHz 옆으로 옮겨 실으면 강한 전력 반송파와 겹치지 않는다", loc="left")
ax.legend(loc="upper left", fontsize=9.5, frameon=True, framealpha=0.95, edgecolor="#ddd")
save(fig, ARTICLE, "spectrum.png")

# 그림 3. ASK-PWM: 높은 구간과 낮은 구간의 '길이 비'로 비트를 싣는다. 클록이 달라도 비는 같다 (원리 그림)
bits = [1, 0, 1, 1, 0]
unit = 1.0  # 비트 하나의 길이 (1 Mbps면 1 µs)
t, env = [0.0], [1.0]
edges = []
for i, b in enumerate(bits):
    start = i * unit
    hi = 0.75 if b else 0.25  # 1은 높은 구간이 길고, 0은 짧다 (규칙은 설명을 위해 단순화)
    edges.append((start, start + hi * unit, b))
    t += [start, start + hi * unit, start + hi * unit, start + unit]
    env += [1.0, 1.0, 0.35, 0.35]
t, env = np.array(t[1:]), np.array(env[1:])
fig, axes = plt.subplots(3, 1, figsize=(9, 4.8), sharex=True, gridspec_kw={"height_ratios": [1.4, 1, 1]})
axes[0].plot(t, env, color=BLUE, lw=2)
for s, e, b in edges:
    axes[0].text((s + s + unit) / 2, 1.12, str(b), ha="center", fontsize=12, fontweight="bold", color=RED)
axes[0].set_ylim(0, 1.35)
axes[0].set_yticks([0.35, 1.0])
axes[0].set_yticklabels(["낮음", "높음"])
axes[0].set_title("하향 신호의 세기(포락선): 비트마다 '높은 구간 : 낮은 구간'의 비가 다르다", loc="left")
for ax, ratio, color, name in [(axes[1], 1.123, TEAL, "칩 A: 클록 +12.3%"), (axes[2], 0.877, ORANGE, "칩 B: 클록 −12.3%")]:
    period = unit / (8 * ratio)  # 비트 하나에 클록이 대략 8번 뛰는 것으로 그렸다
    ticks = np.arange(0, len(bits) * unit, period)
    ax.vlines(ticks, 0, 0.5, color=color, lw=1)
    for s, e, b in edges:
        n_hi = int(np.sum((ticks >= s) & (ticks < e)))
        n_lo = int(np.sum((ticks >= e) & (ticks < s + unit)))
        ax.text(s + unit / 2, 0.72, f"{n_hi}:{n_lo} → {int(n_hi > n_lo)}", ha="center", fontsize=9.5, color=color)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_ylabel(name, rotation=0, ha="right", va="center", fontsize=9.5, color=color)
    ax.grid(False)
axes[2].set_xlabel("시간 (비트)")
axes[2].set_xlim(0, len(bits) * unit)
fig.tight_layout()
save(fig, ARTICLE, "ask-pwm.png")

# 그림 4. 자율 TDMA의 패킷 충돌: 패킷 82 µs, 주기 100 ms
tau, T = 82e-6, 0.1
N = np.arange(2, 301)
slotted = 1 - (1 - tau / T) ** (N - 1)  # 시간 칸이 맞춰져 있을 때
unslotted = 1 - (1 - 2 * tau / T) ** (N - 1)  # 칩마다 클록이 달라 시작 시각이 미끄러질 때
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(N, 100 * unslotted, color=RED, lw=2, label="시작 시각이 칩마다 미끄러질 때 (자유 발진 클록)")
ax.plot(N, 100 * slotted, color=GRAY, lw=1.6, ls="--", label="모두 같은 시간 칸에 맞춰져 있을 때")
ax.plot(64, 100 * 128 / 1160, "o", color=BLUE, ms=8, zorder=5)
ax.annotate("벤치 실측: 칩 64개, 패킷 1,160개 중\n128개 충돌 (11.0%)", xy=(64, 11.0), xytext=(95, 3),
            fontsize=9.5, color=BLUE, arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
for n, label in [(48, "생체 실험 48개"), (100, "논문이 든 한계 약 100개")]:
    ax.axvline(n, color=TEAL, ls=":", lw=1)
    ax.text(n + 2, 34, label, color=TEAL, fontsize=9.5, rotation=90, va="top")
ax.set_xlim(0, 300)
ax.set_ylim(0, 35)
ax.set_xlabel("네트워크의 칩 수")
ax.set_ylabel("패킷이 충돌할 확률 (%)")
ax.set_title("칩이 늘면 충돌이 빠르게 는다 (단순 모형, 직접 계산)", loc="left")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=9.5)
save(fig, ARTICLE, "collision.png")
