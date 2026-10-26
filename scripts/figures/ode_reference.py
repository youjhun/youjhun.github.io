"""MAS201 공학수학 공식집의 그림.

1. 2계 선형계 x'' + 2ζω_n x' + ω_n² x = 0의 자유 응답(x(0)=1, x'(0)=0)과,
   cos ωt로 강제할 때 정상상태 진폭비를 감쇠비별로 그린다.
2. 2×2 선형계 X' = AX의 대표 위상 초상(안장점, 안정 마디점, 안정 나선, 중심)을 그린다.
행렬과 감쇠비는 예로 정한 값이고, 모든 곡선은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()

# 1. 감쇠비에 따른 응답
wn = 1.0
t = np.linspace(0, 20, 1000)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
for z, c in [(0.0, GRAY), (0.2, BLUE), (1.0, TEAL), (2.0, ORANGE)]:
    sol = solve_ivp(lambda tt, y: [y[1], -2 * z * wn * y[1] - wn**2 * y[0]], (0, 20), [1, 0], t_eval=t, rtol=1e-9, atol=1e-12)
    axes[0].plot(t, sol.y[0], color=c, lw=2, label=f"ζ = {z:g}")
axes[0].set_xlabel("시간 $\\omega_n t$")
axes[0].set_ylabel("$x(t)$")
axes[0].set_title("감쇠비에 따른 자유 응답 ($x(0)=1$, $x'(0)=0$)", loc="left")
axes[0].legend(fontsize=9)

r = np.linspace(0, 3, 1200)
for z, c in [(0.1, RED), (0.2, BLUE), (0.5, TEAL), (1.0, ORANGE)]:
    m = 1 / np.sqrt((1 - r**2) ** 2 + (2 * z * r) ** 2)
    axes[1].plot(r, m, color=c, lw=2, label=f"ζ = {z:g}")
axes[1].set_ylim(0, 5.5)
axes[1].set_xlabel("주파수비 $\\omega/\\omega_n$")
axes[1].set_ylabel("진폭비 $\\omega_n^2 A / (F_0/m)$")
axes[1].set_title("강제 진동의 정상상태 진폭비", loc="left")
axes[1].legend(fontsize=9)
fig.tight_layout()
save(fig, "linear-second-order-ode", "damping.png")

for z in (0.1, 0.2, 0.5):
    rp = np.sqrt(1 - 2 * z**2)
    print(f"zeta={z}: peak at r={rp:.3f}, peak ratio={1/(2*z*np.sqrt(1-z**2)):.2f}")

# 2. 위상 초상
cases = [
    ("안장점", np.array([[1.0, 3.0], [3.0, 1.0]])),
    ("안정 마디점", np.array([[-3.0, 1.0], [1.0, -3.0]])),
    ("안정 나선점", np.array([[-1.0, 2.0], [-2.0, -1.0]])),
    ("중심", np.array([[0.0, 2.0], [-2.0, 0.0]])),
]
fig, axes = plt.subplots(1, 4, figsize=(12, 3.3))
g = np.linspace(-2, 2, 17)
Xg, Yg = np.meshgrid(g, g)
for ax, (name, A) in zip(axes, cases):
    U = A[0, 0] * Xg + A[0, 1] * Yg
    V = A[1, 0] * Xg + A[1, 1] * Yg
    if name == "중심":
        # 닫힌 궤도는 streamplot이 끝을 잇지 못해 나선처럼 보이므로 보존량 x² + y²의 등고선으로 그린다
        ax.contour(Xg, Yg, Xg**2 + Yg**2, levels=[0.1, 0.4, 0.9, 1.6, 2.5, 3.6], colors=BLUE, linewidths=0.9)
        ax.quiver(Xg[::2, ::2], Yg[::2, ::2], U[::2, ::2], V[::2, ::2], color=GRAY, angles="xy", scale=60, width=0.006)
    else:
        ax.streamplot(Xg, Yg, U, V, color=BLUE, density=0.9, linewidth=0.8, arrowsize=0.8)
    ev = np.linalg.eigvals(A)
    tr, det = np.trace(A), np.linalg.det(A)
    ax.set_title(f"{name}\n$\\tau={tr:g}$, $\\Delta={det:g}$", loc="left", fontsize=10.5)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    print(name, "trace", tr, "det", round(det, 6), "eig", np.round(ev, 4))
fig.tight_layout()
save(fig, "linear-systems-ode", "phase-portraits.png")
