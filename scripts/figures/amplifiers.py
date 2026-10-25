"""MIT 6.012 단일 트랜지스터 증폭단, 다단 증폭기와 전류 거울 문서의 그림.

소자 값은 예로 정한 것이다: μnCox·W/L = 1 mA/V², VT = 0.5 V, λ = 0.05 V⁻¹,
저항 부하는 출력 바이어스를 0 V로 두는 RD = VDD/ID, VDD = 2.5 V.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

K, VT, LAM, VDD = 1e-3, 0.5, 0.05, 2.5

ARTICLE = "single-stage-amplifiers"
ID = np.logspace(-6, -3, 200)
gm = np.sqrt(2 * K * ID)
ro = 1 / (LAM * ID)
RD = VDD / ID
av_res = gm / (1 / ro + 1 / RD)
av_cs = gm / (2 / ro)  # 같은 λ의 PMOS 전류원: roc = ro
fig, ax = plt.subplots(figsize=(7, 4))
ax.loglog(ID * 1e3, av_cs, color=RED, lw=2, label="전류원 부하: $g_m(r_o\\,/\\!/\\,r_{oc})$")
ax.loglog(ID * 1e3, av_res, color=BLUE, lw=2, label="저항 부하: $g_m(r_o\\,/\\!/\\,R_D)$, $R_D = V_{DD}/I_D$")
ax.set_xlabel("바이어스 전류 $I_D$ (mA)")
ax.set_ylabel("$|A_{vo}|$")
ax.set_title("공통 소스 증폭기의 무부하 전압 이득", loc="left")
ax.legend(fontsize=9.5, loc="upper right")
save(fig, ARTICLE, "cs-gain.png")
i = np.argmin(np.abs(ID - 1e-4))
print(f"at 0.1 mA: resistor {av_res[i]:.1f}, current source {av_cs[i]:.1f}")

ARTICLE = "multistage-amplifiers-current-mirrors"
IREF = 100e-6
vref = VT + np.sqrt(2 * IREF / K)
vout = np.linspace(0, 2.5, 400)
fig, ax = plt.subplots(figsize=(7, 4))
for ratio, c in [(0.5, TEAL), (1.0, BLUE), (2.0, RED)]:
    k2 = K * ratio
    vov = vref - VT
    # λ 항은 VDS = VREF에서 0이 되게 둔다: 그 점에서 iOUT = IREF × (W/L 비)
    sat = k2 / 2 * vov**2 * (1 + LAM * (vout - vref))
    lin = k2 * (vov - vout / 2) * vout * (1 + LAM * (vout - vref))
    iout = np.where(vout < vov, lin, sat)
    ax.plot(vout, iout * 1e6, color=c, lw=2, label=f"$(W/L)_2/(W/L)_1$ = {ratio}")
ax.axvline(vref - VT, color=GRAY, ls=":", lw=1)
ax.text(vref - VT + 0.04, 12, "$V_{DS,sat2}$", color=GRAY, fontsize=9.5)
ax.set_xlabel("출력 전압 $v_{OUT}$ (V)")
ax.set_ylabel("$i_{OUT}$ (µA)")
ax.set_title("NMOS 전류 거울의 출력 특성 ($I_{REF}$ = 100 µA)", loc="left")
ax.legend(fontsize=9.5, loc="lower right")
save(fig, ARTICLE, "mirror-output.png")
print(f"VREF = {vref:.3f} V, ro2(ratio1) = {1/(LAM*IREF)/1e3:.0f} kOhm")
