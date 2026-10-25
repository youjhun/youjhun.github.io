"""MIT 6.012 인버터와 잡음 여유, CMOS 인버터 문서의 그림.

소자 값은 예로 정한 것이다: VDD = 2.5 V, VTn = 0.5 V, VTp = −0.5 V, λ = 0.05 V⁻¹,
kn = μnCox Wn/Ln = 1 mA/V².
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

VDD, VTN, VTP, LAM, KN = 2.5, 0.5, -0.5, 0.05, 1e-3


def nmos(vgs, vds, k=KN, vt=VTN, lam=LAM):
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    if vds < vov:
        return k * (vov - vds / 2) * vds * (1 + lam * vds)
    return k / 2 * vov**2 * (1 + lam * vds)


def pmos(vsg, vsd, k, vt=VTP, lam=LAM):
    return nmos(vsg, vsd, k, -vt, lam)


def cmos_vtc(ratio, vin):
    kp = KN * ratio
    out = []
    for v in vin:
        f = lambda vo: nmos(v, vo) - pmos(VDD - v, VDD - vo, kp)
        out.append(brentq(f, 0.0, VDD))
    return np.array(out)


ARTICLE = "cmos-inverter"
vin = np.linspace(0, VDD, 501)
fig, ax = plt.subplots(figsize=(6.4, 4.4))
for ratio, c, lab in [(0.1, ORANGE, "$k_p/k_n$ = 0.1"), (1.0, BLUE, "$k_p/k_n$ = 1"), (10.0, RED, "$k_p/k_n$ = 10")]:
    ax.plot(vin, cmos_vtc(ratio, vin), color=c, lw=2, label=lab)
ax.plot([0, VDD], [0, VDD], color=GRAY, ls=":", lw=1)
ax.axvline(VTN, color=GRAY, ls="--", lw=0.8)
ax.axvline(VDD + VTP, color=GRAY, ls="--", lw=0.8)
ax.text(VTN + 0.03, 0.1, "$V_{Tn}$", color=GRAY, fontsize=9.5)
ax.text(VDD + VTP + 0.03, 0.1, "$V_{DD} + V_{Tp}$", color=GRAY, fontsize=9.5)
ax.set_xlabel("$V_{IN}$ (V)")
ax.set_ylabel("$V_{OUT}$ (V)")
ax.set_title("CMOS 인버터의 전달 특성", loc="left")
ax.legend(fontsize=9.5, loc="upper right")
save(fig, ARTICLE, "cmos-vtc.png")

ARTICLE = "inverter-noise-margin"
fig, ax = plt.subplots(figsize=(6.4, 4.4))
for R, c in [(2e3, ORANGE), (10e3, BLUE), (50e3, RED)]:
    vo = []
    for v in vin:
        f = lambda x: nmos(v, x) - (VDD - x) / R
        vo.append(brentq(f, 0.0, VDD))
    ax.plot(vin, vo, color=c, lw=2, label=f"R = {R / 1e3:.0f} kΩ")
ax.plot([0, VDD], [0, VDD], color=GRAY, ls=":", lw=1)
ax.set_xlabel("$V_{IN}$ (V)")
ax.set_ylabel("$V_{OUT}$ (V)")
ax.set_title("저항 풀업 NMOS 인버터의 전달 특성", loc="left")
ax.legend(fontsize=9.5, loc="upper right")
save(fig, ARTICLE, "resistor-pullup-vtc.png")
