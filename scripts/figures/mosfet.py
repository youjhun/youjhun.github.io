"""MIT 6.012 MOSFET 전류-전압 특성, 소신호 모델 문서의 그림.

소자 값은 예시로 정한 것이다: μnCox = 100 µA/V², W/L = 10, λ = 0.05 V⁻¹.
문턱전압과 몸체 효과는 MOS 구조 글의 수치 예(γ = 0.42 V^1/2, −2φp = 0.84 V, VTo = 0.26 V)를 쓴다.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

KP = 100e-6 * 10  # μnCox·W/L (A/V²)
VTO = 0.26
GAMMA = 0.42
TWO_PHI = 0.84
LAM = 0.05


def vt(vbs):
    return VTO + GAMMA * (np.sqrt(TWO_PHI - vbs) - np.sqrt(TWO_PHI))


def drain_current(vgs, vds, vbs=0.0, lam=LAM):
    vth = vt(vbs)
    vov = np.maximum(vgs - vth, 0.0)
    lin = KP * (vov - vds / 2) * vds
    sat = KP / 2 * vov**2 * (1 + lam * (vds - vov))
    return np.where(vov <= 0, 0.0, np.where(vds < vov, lin, sat))


ARTICLE = "mosfet-iv"
vds = np.linspace(0, 3, 600)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
colors = [GRAY, TEAL, BLUE, ORANGE, RED]
for vgs, c in zip([0.75, 1.0, 1.25, 1.5, 1.75], colors):
    axes[0].plot(vds, drain_current(vgs, vds) * 1e3, color=c, lw=2, label=f"$V_{{GS}}$ = {vgs} V")
vov = np.linspace(0, 1.6, 100)
axes[0].plot(vov, KP / 2 * vov**2 * 1e3, color=GRAY, ls="--", lw=1)
axes[0].text(1.62, 1.22, "$V_{DS} = V_{GS} - V_T$", color=GRAY, fontsize=9.5)
axes[0].set_xlabel("$V_{DS}$ (V)")
axes[0].set_ylabel("$I_D$ (mA)")
axes[0].set_title("출력 특성", loc="left")
axes[0].legend(fontsize=9, loc="upper left")

vgs = np.linspace(0, 2, 600)
for vbs, c in zip([0, -1, -2, -3], [BLUE, TEAL, ORANGE, RED]):
    axes[1].plot(vgs, drain_current(vgs, 3.0, vbs, lam=0) * 1e3, color=c, lw=2, label=f"$V_{{BS}}$ = {vbs} V, $V_T$ = {vt(vbs):.2f} V")
axes[1].set_xlabel("$V_{GS}$ (V)")
axes[1].set_ylabel("$I_D$ (mA)")
axes[1].set_title("포화 영역의 전달 특성과 몸체 효과", loc="left")
axes[1].legend(fontsize=9, loc="upper left")
fig.tight_layout()
save(fig, ARTICLE, "iv-characteristics.png")

ARTICLE = "mosfet-small-signal"
idc = np.linspace(0, 1.5e-3, 300)
gm = np.sqrt(2 * KP * idc)
go = LAM * idc
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
axes[0].plot(idc * 1e3, gm * 1e3, color=BLUE, lw=2)
axes[0].set_xlabel("$I_D$ (mA)")
axes[0].set_ylabel("$g_m$ (mS)")
axes[0].set_title("포화 영역의 트랜스컨덕턴스", loc="left")
axes[1].plot(idc * 1e3, go * 1e6, color=RED, lw=2)
axes[1].set_xlabel("$I_D$ (mA)")
axes[1].set_ylabel("$g_o$ (µS)")
axes[1].set_title("포화 영역의 출력 컨덕턴스", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "gm-go.png")
print("VT(VBS):", [round(float(vt(v)), 3) for v in (0, -1, -2, -3)])
print("Id(1.25,3)", float(drain_current(1.25, 3.0)), "gm@0.5mA", np.sqrt(2 * KP * 0.5e-3), "go@0.5mA", LAM * 0.5e-3)
