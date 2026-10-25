"""전극–조직 경계 문서의 그림.

원형 전극을 정위상 요소(CPE, 면적에 비례, 지수 n = 0.8)와 확산 저항(지름에 반비례)의 직렬로
단순화해 1 kHz에서의 임피던스와 열잡음을 지름에 따라 계산한다. 값은 모두 예로 정한 것이다:
CPE 계수 20 µF·s^(n−1)/cm², 조직 저항률 3 Ω·m, 체온 310 K, 대역 300 Hz–10 kHz.
표면 거칠기 계수 r은 실제 면적 / 기하 면적이다. 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, ScalarFormatter

from style import BLUE, TEAL, GRAY, save, setup

setup()
ARTICLE = "electrode-tissue-interface"
CDL = 20e-6 * 1e4      # CPE 계수, 면적당 (20 µF·s^(n-1)/cm²)
N_CPE = 0.8
RHO = 3.0              # Ω·m
KB, T = 1.380649e-23, 310.0
F1, F2 = 300.0, 10e3


def z(d, f, rough=1.0):
    area = np.pi * (d / 2) ** 2
    c = CDL * area * rough
    rs = RHO / (2 * d)  # 원판 전극의 확산 저항 ρ/(4a), a = d/2
    return rs + 1 / (c * (1j * 2 * np.pi * f) ** N_CPE), rs


def vnoise(d, rough=1.0):
    f = np.linspace(F1, F2, 4000)
    zz, _ = z(d, f, rough)
    # 열잡음 전력 밀도는 4kT·Re(Z)다. CPE는 실수부를 가져 잡음에 기여한다.
    return np.sqrt(4 * KB * T * np.trapezoid(zz.real, f))


d = np.logspace(np.log10(5e-6), np.log10(200e-6), 200)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
for r, c, name in [(1, BLUE, "매끈한 표면"), (30, TEAL, "거칠기 계수 30")]:
    zz, rs = z(d, 1e3, r)
    axes[0].loglog(d * 1e6, np.abs(zz), color=c, lw=2, label=name)
axes[0].loglog(d * 1e6, RHO / (2 * d), color=GRAY, ls="--", lw=1.2, label="확산 저항")
axes[0].set_xlabel("전극 지름 (µm)")
axes[0].set_ylabel("1 kHz 임피던스 크기 (Ω)")
axes[0].set_title("전극 지름에 따른 임피던스", loc="left")
axes[0].legend(fontsize=9)

dd = np.array([5, 10, 20, 50, 100, 200]) * 1e-6
for r, c, name in [(1, BLUE, "매끈한 표면"), (30, TEAL, "거칠기 계수 30")]:
    axes[1].loglog(d * 1e6, [vnoise(x, r) * 1e6 for x in d], color=c, lw=2, label=name)
axes[1].legend(fontsize=9)
axes[1].yaxis.set_major_formatter(ScalarFormatter())
axes[1].yaxis.set_minor_formatter(NullFormatter())
axes[1].set_xlabel("전극 지름 (µm)")
axes[1].set_ylabel("열잡음 실효값 (µV)")
axes[1].set_title("300 Hz–10 kHz 대역의 열잡음", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "impedance-noise.png")

for x in dd:
    zz, rs = z(x, 1e3)
    zr, _ = z(x, 1e3, 30)
    print(f"d={x*1e6:5.0f} um |Z|={abs(zz)/1e3:9.1f} kOhm  rough30 |Z|={abs(zr)/1e3:8.1f} kOhm  Rs={rs/1e3:6.1f} kOhm  noise={vnoise(x)*1e6:.2f} uV rough30 noise={vnoise(x, 30)*1e6:.2f} uV")
