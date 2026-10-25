"""MIT 6.012 바이폴라 트랜지스터 문서의 그림.

강의의 비선형 하이브리드-π 모형(Ebers-Moll과 같은 식)을 쓴다.
소자 값은 예로 정한 것이다: IS = 1e-16 A, βF = 100, βR = 1, kT/q = 25 mV.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

IS, BF, BR, VTH = 1e-16, 100.0, 1.0, 0.025


def currents(vbe, vbc):
    ebe, ebc = np.exp(vbe / VTH), np.exp(vbc / VTH)
    ic = IS * (ebe - ebc) - IS / BR * (ebc - 1)
    ib = IS / BF * (ebe - 1) + IS / BR * (ebc - 1)
    return ic, ib


ARTICLE = "bjt"
vbe = np.linspace(0.3, 0.85, 400)
ic, ib = currents(vbe, vbe - 3.0)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
axes[0].semilogy(vbe, ic, color=BLUE, lw=2, label="$I_C$")
axes[0].semilogy(vbe, ib, color=RED, lw=2, label="$I_B$")
axes[0].set_xlabel("$V_{BE}$ (V)")
axes[0].set_ylabel("전류 (A)")
axes[0].set_title("검멜 도표 ($V_{CE}$ = 3 V)", loc="left")
axes[0].legend(fontsize=10, loc="upper left")

vce = np.linspace(0, 3, 400)
for ibt, c in zip([20e-6, 40e-6, 60e-6, 80e-6, 100e-6], [GRAY, TEAL, BLUE, ORANGE, RED]):
    out = []
    for v in vce:
        f = lambda x: currents(x, x - v)[1] - ibt
        x = brentq(f, 0.0, 1.2)
        out.append(currents(x, x - v)[0])
    axes[1].plot(vce, np.array(out) * 1e3, color=c, lw=2, label=f"$I_B$ = {ibt * 1e6:.0f} µA")
axes[1].set_xlabel("$V_{CE}$ (V)")
axes[1].set_ylabel("$I_C$ (mA)")
axes[1].set_title("공통 이미터 출력 특성", loc="left")
axes[1].legend(fontsize=9, loc="center left", bbox_to_anchor=(1.01, 0.5))
fig.tight_layout()
save(fig, ARTICLE, "gummel-output.png")

v = brentq(lambda x: currents(x, x - 3.0)[0] - 1e-3, 0.3, 1.0)
print(f"VBE for IC=1mA: {v:.3f} V")
vsat = brentq(lambda x: currents(x, x - 0.2)[1] - 100e-6, 0, 1.2)
print("IC at VCE=0.2, IB=100uA", currents(vsat, vsat - 0.2)[0])
