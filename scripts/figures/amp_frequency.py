"""MIT 6.012 증폭기의 주파수 응답 문서의 그림.

소자 값은 예로 정한 것이다: gm = 1 mS, Cgs = 50 fF, Cgd = 5 fF, Cdb = 10 fF,
RS = 10 kΩ, R'out = 100 kΩ. 캐스코드 어림에서는 두 트랜지스터에 같은 값을 쓰고 Csb = 0으로 둔다.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

GM, CGS, CGD, CDB, RS = 1e-3, 50e-15, 5e-15, 10e-15, 10e3


def cs_exact(w, rout):
    num = -(GM - 1j * w * CGD) * rout
    den = 1 + 1j * w * (RS * CGS + RS * CGD * (1 + rout * (1 / RS + GM)) + rout * CDB) - w**2 * RS * rout * CGS * (CGD + CDB)
    return num / den


def oct_tau(rout):
    return RS * CGS + (rout + RS * (1 + GM * rout)) * CGD + rout * CDB


ARTICLE = "amplifier-frequency-response"
f = np.logspace(5, 11, 800)
w = 2 * np.pi * f
ROUT = 100e3
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
axes[0].loglog(f, np.abs(cs_exact(w, ROUT)), color=BLUE, lw=2, label="전달함수 그대로")
fh = 1 / (2 * np.pi * oct_tau(ROUT))
axes[0].loglog(f, GM * ROUT / np.sqrt(1 + (f / fh) ** 2), color=ORANGE, lw=1.6, ls="--", label="개방 시상수 근사")
axes[0].axvline(fh, color=GRAY, ls=":", lw=1)
axes[0].text(fh * 1.3, 2, f"$f_H$ ≈ {fh / 1e6:.0f} MHz", color=GRAY, fontsize=9.5)
axes[0].set_xlabel("주파수 (Hz)")
axes[0].set_ylabel("$|A_v|$")
axes[0].set_title("공통 소스 증폭기의 전압 이득", loc="left")
axes[0].legend(fontsize=9.5, loc="lower left")

rout = np.logspace(3.5, 6, 100)
alf = GM * rout
fhs = 1 / (2 * np.pi * np.array([oct_tau(r) for r in rout]))
axes[1].loglog(alf, fhs / 1e6, color=RED, lw=2, label="$f_H$")
axes[1].loglog(alf, alf * fhs / 1e6, color=TEAL, lw=2, label="$|A_{v,LF}|\\,f_H$")
axes[1].set_xlabel("저주파 이득 $|A_{v,LF}| = g_m R'_{out}$")
axes[1].set_ylabel("MHz")
axes[1].set_title("저주파 이득에 따른 대역폭", loc="left")
axes[1].legend(fontsize=9.5)
fig.tight_layout()
save(fig, ARTICLE, "cs-bandwidth.png")

ft = GM / (2 * np.pi * (CGS + CGD))
taus = (RS * CGS, (ROUT + RS * (1 + GM * ROUT)) * CGD, ROUT * CDB)
print(f"fT = {ft/1e9:.2f} GHz, fH = {fh/1e6:.1f} MHz, taus (ns) = {[round(t*1e9,2) for t in taus]}")
print(f"Miller C = {CGD*(1+GM*ROUT)*1e15:.0f} fF")
# 캐스코드: τgd1 ≈ [1/gm2 + RS(1 + gm1/gm2)]Cgd1 (gmb 무시), 출력 마디는 같은 R'out에 Cgd2 + Cdb2
tau_c = RS * CGS + (1 / GM + RS * 2) * CGD + (1 / GM) * (CDB + CGS) + ROUT * (CGD + CDB)
print(f"cascode fH ≈ {1/(2*np.pi*tau_c)/1e6:.0f} MHz")
