"""커패시터·인덕터, RC·RL 1차 회로 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

# 커패시터와 인덕터: 같은 전류 파형을 넣었을 때 전압이 어떻게 나오는가
ARTICLE = "capacitors-inductors"
t = np.linspace(0, 4, 4001)  # ms
i_sq = np.where((t % 2) < 1, 1.0, -1.0)  # mA, 1 ms마다 부호가 바뀌는 사각파
C = 1.0  # µF
v_c = np.cumsum(i_sq) * (t[1] - t[0]) / C  # mA·ms/µF = V
v_c -= v_c.mean()
i_tri = np.cumsum(i_sq) * (t[1] - t[0])  # mA, 삼각파
i_tri -= i_tri.mean()
L = 100.0  # mH
v_l = L * np.gradient(i_tri, t) / 1000  # mH·mA/ms = mV → V
fig, axes = plt.subplots(2, 2, figsize=(10, 4.6), sharex=True)
axes[0, 0].plot(t, i_sq, color=BLUE, lw=1.8)
axes[0, 0].set_title("커패시터 C = 1 µF에 흘린 전류", loc="left")
axes[0, 0].set_ylabel("전류 (mA)")
axes[1, 0].plot(t, v_c, color=RED, lw=1.8)
axes[1, 0].set_title("커패시터 전압: 전류를 적분한 모양", loc="left")
axes[1, 0].set_ylabel("전압 (V)")
axes[0, 1].plot(t, i_tri, color=BLUE, lw=1.8)
axes[0, 1].set_title("인덕터 L = 100 mH에 흘린 전류", loc="left")
axes[1, 1].plot(t, v_l, color=TEAL, lw=1.8)
axes[1, 1].set_title("인덕터 전압: 전류를 미분한 모양", loc="left")
for ax in axes[1]:
    ax.set_xlabel("시간 (ms)")
fig.tight_layout()
save(fig, ARTICLE, "integrate-differentiate.png")

# RC·RL 1차 회로: 계단 응답과 시간상수
ARTICLE = "first-order-rc-rl"
tau = 1.0
t = np.linspace(0, 6, 1201)
v = 1 - np.exp(-t / tau)
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(t, v, color=BLUE, lw=2, label="충전: $v_C/V_s = 1 - e^{-t/\\tau}$")
ax.plot(t, 1 - v, color=ORANGE, lw=2, label="방전: $v_C/V_0 = e^{-t/\\tau}$")
for k in range(1, 6):
    ax.axvline(k, color="#ddd", lw=1, zorder=0)
    ax.text(k, 1.04, f"{k}τ", ha="center", fontsize=9.5, color=GRAY)
    ax.plot(k, 1 - np.exp(-k), "o", color=BLUE, ms=5)
ax.annotate(f"{100 * (1 - np.exp(-1)):.1f}%", xy=(1, 1 - np.exp(-1)), xytext=(1.25, 0.5), color=BLUE, fontsize=10,
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
ax.annotate(f"{100 * (1 - np.exp(-5)):.1f}%", xy=(5, 1 - np.exp(-5)), xytext=(4.3, 0.78), color=BLUE, fontsize=10,
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
ax.set_xlim(0, 6)
ax.set_ylim(0, 1.1)
ax.set_xlabel("시간 (τ 단위)")
ax.set_ylabel("정규화한 커패시터 전압")
ax.set_title("1차 회로의 계단 응답과 시간상수 τ", loc="left")
ax.legend(loc="center right", fontsize=10)
save(fig, ARTICLE, "step-response.png")

# RC 저역통과·고역통과의 주파수 응답 (R = 10 kΩ, C = 100 nF → f_c ≈ 159 Hz)
R, Cf = 10e3, 100e-9
fc = 1 / (2 * np.pi * R * Cf)
f = np.logspace(0, 5, 600)
s = 1j * 2 * np.pi * f * R * Cf
H_lp = 1 / (1 + s)
H_hp = s / (1 + s)
fig, axes = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
for H, color, label in [(H_lp, BLUE, "저역통과 (C 양단에서 출력)"), (H_hp, RED, "고역통과 (R 양단에서 출력)")]:
    axes[0].semilogx(f, 20 * np.log10(np.abs(H)), color=color, lw=2, label=label)
    axes[1].semilogx(f, np.degrees(np.angle(H)), color=color, lw=2)
for ax in axes:
    ax.axvline(fc, color=GRAY, ls=":", lw=1.2)
axes[0].axhline(-3.01, color=GRAY, ls="--", lw=1)
axes[0].text(fc * 0.85, -20, f"$f_c$ = {fc:.0f} Hz", color=GRAY, fontsize=10, ha="right")
axes[0].text(1.3, -8, "−3 dB", color=GRAY, fontsize=9.5)
axes[0].set_ylim(-60, 5)
axes[0].set_ylabel("크기 (dB)")
axes[0].set_title("RC 1차 필터의 주파수 응답 (R = 10 kΩ, C = 100 nF)", loc="left")
axes[0].legend(loc="lower center", fontsize=9.5)
axes[1].set_yticks([-90, -45, 0, 45, 90])
axes[1].set_ylabel("위상 (°)")
axes[1].set_xlabel("주파수 (Hz)")
fig.tight_layout()
save(fig, ARTICLE, "rc-bode.png")
