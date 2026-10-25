"""무선 전력과 원격 측정 문서의 그림.

같은 축 위에 놓인 두 원형 고리의 상호 인덕턴스를 타원 적분으로 계산해 결합 계수 k를 구하고,
최적 부하에서의 최대 링크 효율 η = k²Q1Q2 / (1 + √(1 + k²Q1Q2))²를 그린다.
고리 반지름, 도선 반지름, Q 값은 예로 정한 것이고, 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ellipk, ellipe

from style import BLUE, ORANGE, TEAL, save, setup

setup()
ARTICLE = "wireless-power-telemetry"
MU0 = 4e-7 * np.pi
A_WIRE = 0.1e-3  # 도선 반지름


def self_l(r):
    return MU0 * r * (np.log(8 * r / A_WIRE) - 2)


def mutual(r1, r2, d):
    m = 4 * r1 * r2 / ((r1 + r2) ** 2 + d**2)
    k = np.sqrt(m)
    return MU0 * np.sqrt(r1 * r2) * ((2 / k - k) * ellipk(m) - 2 / k * ellipe(m))


def coupling(r1, r2, d):
    return mutual(r1, r2, d) / np.sqrt(self_l(r1) * self_l(r2))


def eta(k, q1, q2):
    x = k**2 * q1 * q2
    return x / (1 + np.sqrt(1 + x)) ** 2


R1 = 15e-3
d = np.linspace(1e-3, 40e-3, 400)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
for r2, c in [(10e-3, BLUE), (3e-3, TEAL), (1e-3, ORANGE)]:
    axes[0].semilogy(d * 1e3, coupling(R1, r2, d), color=c, lw=2, label=f"이식 고리 반지름 {r2*1e3:g} mm")
axes[0].set_xlabel("고리 사이 거리 (mm)")
axes[0].set_ylabel("결합 계수 $k$")
axes[0].set_title("외부 고리 반지름 15 mm일 때의 결합 계수", loc="left")
axes[0].legend(fontsize=9)

kk = np.logspace(-4, 0, 400)
for q, c in [(10, ORANGE), (50, TEAL), (200, BLUE)]:
    axes[1].semilogx(kk, eta(kk, q, q) * 100, color=c, lw=2, label=f"$Q_1 = Q_2 = {q}$")
axes[1].set_xlabel("결합 계수 $k$")
axes[1].set_ylabel("최대 링크 효율 (%)")
axes[1].set_title("결합 계수와 Q에 따른 최대 링크 효율", loc="left")
axes[1].legend(fontsize=9)
fig.tight_layout()
save(fig, ARTICLE, "coupling-efficiency.png")

for r2 in (10e-3, 3e-3, 1e-3):
    for dd in (5e-3, 10e-3, 20e-3):
        k = coupling(R1, r2, dd)
        print(f"r2={r2*1e3:g} mm d={dd*1e3:g} mm k={k:.4f} eta(Q=50)={eta(k,50,50)*100:.1f}% eta(Q=200)={eta(k,200,200)*100:.1f}%")
