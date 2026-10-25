"""MIT 6.012 pn 다이오드 문서의 그림.

소자 값은 예로 정한 것이다: 면적 A = 100 µm × 100 µm, Na = 1e17, Nd = 1e16 cm⁻³,
Dn = 25, Dp = 10 cm²/s, 두 준중성 영역의 폭 1 µm, ni = 1e10 cm⁻³, kT/q = 25 mV.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

q, ni, VTH = 1.602e-19, 1e10, 0.025
eps_s = 11.7 * 8.854e-14
A = (100e-4) ** 2  # cm²
Na, Nd, Dn, Dp, Wp, Wn = 1e17, 1e16, 25.0, 10.0, 1e-4, 1e-4
phiB = 0.060 * (np.log10(Na / ni) + np.log10(Nd / ni))
In0 = q * A * ni**2 * Dn / (Na * Wp)
Ip0 = q * A * ni**2 * Dp / (Nd * Wn)
Io = In0 + Ip0
tauTn = Wp**2 / (2 * Dn)
tauTp = Wn**2 / (2 * Dp)
tauT = (tauTn * In0 + tauTp * Ip0) / Io
Cjo = A * np.sqrt(q * eps_s * Na * Nd / (2 * phiB * (Na + Nd)))

ARTICLE = "pn-diode"
V = np.linspace(-0.3, 0.75, 800)
I = Io * (np.exp(V / VTH) - 1)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
axes[0].plot(V, I * 1e3, color=BLUE, lw=2)
axes[0].set_ylim(-0.2, 5)
axes[0].set_xlabel("V (V)")
axes[0].set_ylabel("I (mA)")
axes[0].set_title("선형 축", loc="left")
axes[1].semilogy(V, np.abs(I), color=RED, lw=2)
axes[1].axhline(Io, color=GRAY, ls="--", lw=1)
axes[1].text(-0.28, Io * 3, f"$I_o$ = {Io:.1e} A", color=GRAY, fontsize=9.5)
axes[1].set_xlabel("V (V)")
axes[1].set_ylabel("|I| (A)")
axes[1].set_title("반로그 축 (60 mV마다 10배)", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "iv.png")

V2 = np.linspace(-3, 0.7, 800)
Cj = Cjo / np.sqrt(1 - np.minimum(V2, phiB / 2) / phiB)
Iv = Io * (np.exp(V2 / VTH) - 1)
Cd = tauT * np.maximum(Iv + Io, 0) / VTH
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.semilogy(V2, Cj * 1e12, color=BLUE, lw=2, label="공핍 커패시턴스 $C_j$")
ax.semilogy(V2, np.maximum(Cd, 1e-18) * 1e12, color=RED, lw=2, label="확산 커패시턴스 $C_d$")
ax.axvline(phiB / 2, color=GRAY, ls=":", lw=1)
ax.text(phiB / 2 - 0.05, 30, "$\\phi_B/2$", color=GRAY, fontsize=9.5, ha="right")
ax.set_ylim(1e-3, 1e3)
ax.set_xlabel("V (V)")
ax.set_ylabel("커패시턴스 (pF)")
ax.set_title("바이어스에 따른 두 커패시턴스", loc="left")
ax.legend(fontsize=9.5, loc="upper left")
save(fig, ARTICLE, "capacitances.png")

cross = V2[np.argmin(np.abs(np.log(np.maximum(Cd, 1e-30)) - np.log(Cj)))]
print(f"phiB={phiB:.3f} Io={Io:.3e} In0/Io={In0/Io:.2f} tauT={tauT*1e12:.0f}ps Cjo={Cjo*1e12:.2f}pF cross={cross:.3f}V")
print("I at 0.6V", Io * np.exp(0.6 / VTH), "gd at 1mA", 1e-3 / VTH)
