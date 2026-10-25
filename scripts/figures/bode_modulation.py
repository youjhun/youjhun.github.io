"""보드 선도, 변조 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

# 보드 선도: H(s) = 10s / ((s+1)(s+10))
ARTICLE = "bode-plot"
w = np.logspace(-2, 3, 1000)
s = 1j * w
H = 10 * s / ((s + 1) * (s + 10))
mag = 20 * np.log10(np.abs(H))
# 직선 근사: 영점 0(+20 dB/dec), 극점 1과 10에서 꺾임, 저주파에서 10s/10 = s
asym = np.where(w < 1, 20 * np.log10(w), np.where(w < 10, 0, -20 * np.log10(w / 10)))
ph = np.degrees(np.angle(H))


def phase_asym(w, p):
    """극점 하나의 위상 직선 근사: p/10까지 0, 10p부터 −90°, 그 사이는 log ω에 비례."""
    return np.where(w < p / 10, 0, np.where(w > 10 * p, -90, -45 * (np.log10(w / p) + 1)))


ph_asym = 90 + phase_asym(w, 1) + phase_asym(w, 10)
fig, axes = plt.subplots(2, 1, figsize=(8, 5.4), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
axes[0].semilogx(w, mag, color=BLUE, lw=2, label="실제 크기")
axes[0].semilogx(w, asym, color=ORANGE, lw=1.5, ls="--", label="직선 근사")
axes[0].set_ylabel("크기 (dB)")
axes[0].set_ylim(-45, 5)
axes[0].set_title("H(s) = 10s / ((s + 1)(s + 10))의 보드 선도", loc="left")
axes[0].legend(loc="lower center", fontsize=10)
axes[1].semilogx(w, ph, color=BLUE, lw=2)
axes[1].semilogx(w, ph_asym, color=ORANGE, lw=1.5, ls="--")
axes[1].set_yticks([-90, -45, 0, 45, 90])
axes[1].set_ylabel("위상 (°)")
axes[1].set_xlabel("ω (rad/s)")
for ax in axes:
    for c in (1, 10):
        ax.axvline(c, color=GRAY, ls=":", lw=1)
fig.tight_layout()
save(fig, ARTICLE, "bode-example.png")

# 2차 시스템: Q에 따른 공진
wn = np.logspace(-1, 1, 2000)
fig, axes = plt.subplots(2, 1, figsize=(8, 5.4), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
for Q, color in [(0.5, GRAY), (1, TEAL), (3, ORANGE), (10, RED)]:
    Hq = 1 / (1 - wn**2 + 1j * wn / Q)
    axes[0].semilogx(wn, 20 * np.log10(np.abs(Hq)), color=color, lw=1.8, label=f"Q = {Q}")
    axes[1].semilogx(wn, np.degrees(np.angle(Hq)), color=color, lw=1.8)
axes[0].set_ylabel("크기 (dB)")
axes[0].set_ylim(-40, 25)
axes[0].set_title("2차 시스템 1/(1 + s/(Qω₀) + (s/ω₀)²)의 주파수 응답", loc="left")
axes[0].legend(loc="lower left", fontsize=10)
axes[1].set_yticks([-180, -90, 0])
axes[1].set_ylabel("위상 (°)")
axes[1].set_xlabel("ω / ω₀")
fig.tight_layout()
save(fig, ARTICLE, "high-q.png")

# 변조: 진폭 변조와 동기 복조의 스펙트럼
ARTICLE = "modulation"
f = np.linspace(-3.2, 3.2, 3201)
msg = np.clip(1 - np.abs(f) / 0.4, 0, None)  # 대역 제한 메시지(삼각형 스펙트럼)
fc = 1.0


def shifted(f0):
    return np.clip(1 - np.abs(f - f0) / 0.4, 0, None)


Y = 0.5 * (shifted(fc) + shifted(-fc))
Z = 0.5 * msg + 0.25 * (shifted(2 * fc) + shifted(-2 * fc))
fig, axes = plt.subplots(3, 1, figsize=(8.5, 5.6), sharex=True)
axes[0].fill_between(f, msg, color=BLUE, alpha=0.8)
axes[0].set_title("메시지 X(jω)", loc="left")
axes[1].fill_between(f, Y, color=TEAL, alpha=0.8)
axes[1].set_title("변조한 신호 $Y(j\\omega)$, $y(t) = x(t)\\cos\\omega_c t$", loc="left")
axes[2].fill_between(f, Z, color=ORANGE, alpha=0.8)
lpf = (np.abs(f) <= 0.5).astype(float) * 0.62
axes[2].plot(f, lpf, color=RED, lw=1.5, ls="--", label="저역통과 필터")
axes[2].legend(loc="upper right", fontsize=9.5)
axes[2].set_title("복조 곱셈 뒤 $Z(j\\omega)$, $z(t) = y(t)\\cos\\omega_c t$", loc="left")
axes[2].set_xticks([-2 * fc, -fc, 0, fc, 2 * fc])
axes[2].set_xticklabels([r"$-2\omega_c$", r"$-\omega_c$", "0", r"$\omega_c$", r"$2\omega_c$"])
axes[2].set_xlabel("ω")
for ax in axes:
    ax.set_yticks([])
    ax.set_ylim(0, 1.15)
fig.tight_layout()
save(fig, ARTICLE, "am-spectrum.png")

# FM: 변조 지수 m에 따른 스펙트럼 선(베셀 함수 계수)
fig, axes = plt.subplots(1, 3, figsize=(10, 3.0), sharey=True)
for ax, m in zip(axes, [1, 5, 20]):
    k = np.arange(-30, 31)
    ax.vlines(k, 0, np.abs(jv(k, m)), color=BLUE, lw=1.6)
    ax.axvspan(-(m + 1), m + 1, color="#eef3f6", zorder=0)
    ax.set_title(f"m = {m}", loc="left")
    ax.set_xlabel(r"반송파에서 떨어진 정도 ($\omega_m$ 단위)")
axes[0].set_ylabel("선 스펙트럼의 크기")
fig.suptitle(r"$\cos(\omega_c t + m\sin\omega_m t)$의 스펙트럼 (음영: $\pm(m+1)\omega_m$)", x=0.01, ha="left", fontweight="bold", fontsize=12.5)
fig.tight_layout()
save(fig, ARTICLE, "fm-spectrum.png")
