"""MIT 6.012 반도체 캐리어, pn 접합 정전기, MOS 구조와 문턱전압 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

q = 1.602e-19
eps0 = 8.854e-14  # F/cm
eps_s = 11.7 * eps0
eps_ox = 3.9 * eps0
ni = 1e10  # cm^-3, Si 300 K
VT_TH = 0.025  # kT/q 근사, 강의 자료와 같은 값

# 캐리어 농도: n형 도핑 농도에 따른 평형 전자·정공 농도
ARTICLE = "semiconductor-carriers"
Nd = np.logspace(6, 20, 400)
n0 = Nd / 2 + np.sqrt((Nd / 2) ** 2 + ni**2)
p0 = ni**2 / n0
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.loglog(Nd, n0, color=BLUE, lw=2, label="전자 $n_o$ (다수 캐리어)")
ax.loglog(Nd, p0, color=RED, lw=2, label="정공 $p_o = n_i^2/n_o$ (소수 캐리어)")
ax.axvline(ni, color=GRAY, ls=":", lw=1.2)
ax.text(ni * 1.4, 1e17, "$N_d = n_i$", color=GRAY, fontsize=10)
ax.text(1e7, 3e11, "진성", color=GRAY, fontsize=10.5)
ax.text(1e15, 3e10, "외인성", color=GRAY, fontsize=10.5)
ax.set_xlabel("도너 농도 $N_d$ (cm$^{-3}$)")
ax.set_ylabel("평형 농도 (cm$^{-3}$)")
ax.set_title("n형 실리콘의 평형 캐리어 농도 (300 K, $n_i = 10^{10}$ cm$^{-3}$)", loc="left")
ax.legend(loc="lower left", fontsize=10)
save(fig, ARTICLE, "carrier-concentration.png")

# pn 접합: 공핍 근사의 전하, 전기장, 전위 (Na = 1e17, Nd = 1e15)
ARTICLE = "pn-junction-electrostatics"
Na, Nd1 = 1e17, 1e15
phi_p = -0.060 * np.log10(Na / ni)
phi_n = 0.060 * np.log10(Nd1 / ni)
phiB = phi_n - phi_p
xno = np.sqrt(2 * eps_s * phiB * Na / (q * (Na + Nd1) * Nd1))
xpo = xno * Nd1 / Na
x = np.linspace(-0.4e-4, 1.4e-4, 4000)
rho = np.where((x > -xpo) & (x < 0), -q * Na, np.where((x >= 0) & (x < xno), q * Nd1, 0.0))
E = np.where((x > -xpo) & (x < 0), -q * Na / eps_s * (x + xpo), np.where((x >= 0) & (x < xno), q * Nd1 / eps_s * (x - xno), 0.0))
phi = np.where(x <= -xpo, phi_p, np.where(x < 0, phi_p + q * Na / (2 * eps_s) * (x + xpo) ** 2,
               np.where(x < xno, phi_n - q * Nd1 / (2 * eps_s) * (x - xno) ** 2, phi_n)))
xu = x * 1e4  # µm
fig, axes = plt.subplots(3, 1, figsize=(8, 6.2), sharex=True)
axes[0].fill_between(xu, rho / q, color=TEAL, alpha=0.8, step="mid")
axes[0].set_yscale("symlog", linthresh=1e15)
axes[0].set_yticks([-1e17, -1e16, -1e15, 0, 1e15])
axes[0].set_yticklabels(["$-10^{17}$", "$-10^{16}$", "$-10^{15}$", "0", "$10^{15}$"])
axes[0].set_ylabel("ρ/q (cm$^{-3}$)")
axes[0].set_title("공간전하 밀도", loc="left")
axes[1].plot(xu, E / 1e3, color=BLUE, lw=2)
axes[1].set_ylabel("E (kV/cm)")
axes[1].set_title("전기장", loc="left")
axes[2].plot(xu, phi * 1e3, color=RED, lw=2)
axes[2].set_ylabel("φ (mV)")
axes[2].set_title("정전기 전위", loc="left")
axes[2].set_xlabel("위치 x (µm), 0은 금속학적 접합")
for ax in axes:
    ax.axvline(0, color=GRAY, ls=":", lw=1)
fig.suptitle("공핍 근사로 푼 계단형 pn 접합 ($N_a = 10^{17}$, $N_d = 10^{15}$ cm$^{-3}$, 평형)", x=0.01, ha="left", fontweight="bold", fontsize=12.5)
fig.tight_layout()
save(fig, ARTICLE, "depletion-approximation.png")

# 공핍 커패시턴스: Cj(V)와 1/Cj^2
V = np.linspace(-5, 0.5, 400)
xd = np.sqrt(2 * eps_s * (phiB - V) * (Na + Nd1) / (q * Na * Nd1))
Cj = eps_s / xd
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
axes[0].plot(V, Cj * 1e9, color=BLUE, lw=2)
axes[0].set_xlabel("인가 전압 V (V)")
axes[0].set_ylabel("$C_j$ (nF/cm$^2$)")
axes[0].set_title("공핍 커패시턴스", loc="left")
axes[1].plot(V, 1 / Cj**2 / 1e16, color=RED, lw=2)
Ve = np.linspace(0.5, phiB, 20)
axes[1].plot(Ve, 2 * (phiB - Ve) * (Na + Nd1) / (q * eps_s * Na * Nd1) / 1e16, color=RED, lw=1.2, ls="--")
axes[1].axvline(phiB, color=GRAY, ls=":", lw=1.2)
axes[1].text(phiB - 0.15, 4.5, f"$\\phi_B$ = {phiB * 1e3:.0f} mV", color=GRAY, fontsize=9.5, ha="right")
axes[1].set_xlim(-5.2, 1.0)
axes[1].set_ylim(0, None)
axes[1].set_xlabel("인가 전압 V (V)")
axes[1].set_ylabel("$1/C_j^2$ ($10^{16}$ cm$^4$/F$^2$)")
axes[1].set_title("$1/C_j^2$ 대 V", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "depletion-capacitance.png")

# MOS: 게이트 전압에 따른 공핍층 두께와 반전 전하
ARTICLE = "mos-capacitor-threshold"
tox, NaM = 8e-7, 1e17
Cox = eps_ox / tox
gamma = np.sqrt(2 * eps_s * q * NaM) / Cox
phi_pM = -0.060 * np.log10(NaM / ni)
phiBM = 0.550 - phi_pM
VFB = -phiBM
VT = VFB - 2 * phi_pM + gamma * np.sqrt(-2 * phi_pM)
xdmax = np.sqrt(2 * eps_s * (-2 * phi_pM) / (q * NaM))
Vg = np.linspace(-1.6, 1.6, 800)
xdV = np.where(Vg <= VFB, 0.0, eps_s / Cox * (np.sqrt(1 + 4 * np.clip(Vg - VFB, 0, None) / gamma**2) - 1))
xdV = np.minimum(xdV, xdmax)
Qn = np.where(Vg > VT, Cox * (Vg - VT), 0.0)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
axes[0].plot(Vg, xdV * 1e7, color=BLUE, lw=2)
axes[0].axhline(xdmax * 1e7, color=GRAY, ls="--", lw=1)
axes[0].set_ylabel("공핍층 두께 $x_d$ (nm)")
axes[0].set_title("공핍층 두께", loc="left")
axes[1].plot(Vg, Qn * 1e6, color=RED, lw=2)
axes[1].set_ylabel("$|Q_n|$ (µC/cm$^2$)")
axes[1].set_title("반전층 전하 (전하 제어 관계)", loc="left")
for ax in axes:
    ax.axvline(VFB, color=GRAY, ls=":", lw=1.2)
    ax.axvline(VT, color=ORANGE, ls=":", lw=1.2)
    ax.set_xlabel("게이트-기판 전압 $V_{GB}$ (V)")
axes[0].text(VFB - 0.05, xdmax * 1e7 * 0.5, "$V_{FB}$", color=GRAY, ha="right", fontsize=10)
axes[0].text(VT + 0.05, xdmax * 1e7 * 0.5, "$V_T$", color=ORANGE, fontsize=10)
axes[0].text(-1.55, xdmax * 1e7 * 1.03, "축적", color=GRAY, fontsize=9.5)
axes[0].text(-0.55, xdmax * 1e7 * 1.03, "공핍", color=GRAY, fontsize=9.5)
axes[0].text(0.75, xdmax * 1e7 * 1.03, "반전", color=GRAY, fontsize=9.5)
axes[0].set_ylim(0, xdmax * 1e7 * 1.15)
fig.tight_layout()
save(fig, ARTICLE, "mos-regimes.png")
print(f"phiB(pn)={phiB:.3f} xno={xno*1e4:.3f}um xpo={xpo*1e7:.1f}nm; MOS Cox={Cox:.3e} gamma={gamma:.3f} VT={VT:.3f} xdmax={xdmax*1e7:.0f}nm")
