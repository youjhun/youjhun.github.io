"""이산시간 푸리에 변환(DTFT) 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, pi_ticks, save, setup

ARTICLE = "dtft"
setup()

# 그림 1. 단위원 위를 도는 e^{jω}
fig, ax = plt.subplots(figsize=(5.2, 5.2))
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color=BLUE, lw=2)
ax.axhline(0, color="#777", lw=0.8)
ax.axvline(0, color="#777", lw=0.8)
w = np.pi / 3
ax.plot([0, np.cos(w)], [0, np.sin(w)], color=RED, lw=1.6)
ax.plot(np.cos(w), np.sin(w), "o", color=RED, ms=8)
ax.text(np.cos(w) + 0.06, np.sin(w) + 0.06, r"$e^{j\omega}$", color=RED, fontsize=14)
arc = np.linspace(0, w, 50)
ax.plot(0.28 * np.cos(arc), 0.28 * np.sin(arc), color=RED, lw=1.2)
ax.text(0.33, 0.12, "ω", color=RED, fontsize=13)
ax.plot(1, 0, "s", color=TEAL, ms=8)
ax.text(1.04, -0.09, "ω = 0\n(가장 느린 변화, DC)", color=TEAL, fontsize=10, va="top")
ax.plot(-1, 0, "s", color=ORANGE, ms=8)
ax.text(-1.62, -0.09, "ω = π\n(가장 빠른 변화)", color=ORANGE, fontsize=10, va="top")
ax.annotate("", xy=(np.cos(2.3), np.sin(2.3)), xytext=(np.cos(1.6), np.sin(1.6)),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4, connectionstyle="arc3,rad=0.25"))
ax.text(-0.15, 1.12, "ω가 커지면 반시계 방향으로 돈다", color=GRAY, fontsize=9.5, ha="center")
ax.text(0.15, -0.55, "ω와 ω + 2π는\n같은 점이다", color=BLUE, fontsize=10, ha="center")
ax.set_xlim(-1.7, 1.75)
ax.set_ylim(-1.35, 1.35)
ax.set_aspect("equal")
ax.set_xlabel("실수부")
ax.set_ylabel("허수부")
ax.set_title("z 평면의 단위원과 주파수 ω")
ax.grid(False)
save(fig, ARTICLE, "unit-circle.png")

# 그림 2. 길이 5인 사각 펄스의 DTFT 크기는 2π마다 반복된다
w = np.linspace(-3 * np.pi, 3 * np.pi, 6000)
L = 5
with np.errstate(divide="ignore", invalid="ignore"):
    mag = np.abs(np.sin(L * w / 2) / np.sin(w / 2))
mag[np.isnan(mag)] = L
fig, ax = plt.subplots(figsize=(8.5, 3.2))
ax.axvspan(-np.pi, np.pi, color=LIGHT, zorder=0, label="한 주기 [−π, π]")
ax.plot(w, mag, color=BLUE, lw=1.8, label=r"$|X(e^{j\omega})|$")
ax.set_ylabel("크기")
ax.set_xlabel("ω (rad/표본)")
pi_ticks(ax, -3, 3)
ax.set_title("x[n] = 1 (n = 0, …, 4)의 DTFT 크기: 2π마다 같은 모양이 되풀이된다")
ax.legend(loc="upper right", fontsize=9.5)
ax.set_ylim(0, 6.2)
save(fig, ARTICLE, "periodic-spectrum.png")

# 그림 3. 이산시간에서 '빠름'의 끝은 π다
n = np.arange(0, 17)
cases = [
    (0, "ω = 0"),
    (np.pi / 4, "ω = π/4"),
    (np.pi, "ω = π (가장 빠름)"),
    (7 * np.pi / 4, "ω = 7π/4 (= −π/4, 다시 느려짐)"),
]
fig, axes = plt.subplots(4, 1, figsize=(8, 7.4), sharex=True)
for ax, (om, label) in zip(axes, cases):
    y = np.cos(om * n)
    color = RED if om == np.pi else BLUE
    ax.vlines(n, 0, y, color=color, lw=1.4)
    ax.plot(n, y, "o", color=color, ms=4.5)
    ax.axhline(0, color="#777", lw=0.7)
    ax.set_ylim(-1.35, 1.35)
    ax.set_yticks([-1, 0, 1])
    ax.set_title(f"cos(ωn),  {label}", loc="left", fontsize=10.5, fontweight="normal", color=color)
axes[-1].set_xlabel("n")
fig.suptitle("ω를 키우면 π까지는 빨라지고, 그 뒤로는 도로 느려진다", fontweight="bold", y=0.995)
fig.tight_layout()
save(fig, ARTICLE, "dt-frequencies.png")
