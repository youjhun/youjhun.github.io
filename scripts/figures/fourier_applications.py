"""MIT 6.003 푸리에 변환의 응용 문서의 그림.

RC 저역통과 필터에 사각파를 넣은 출력을 푸리에 급수로 계산하고, 심전도 잡음 제거용
필터(고역통과 + 저역통과 + 노치)의 크기 응답을 그린다. 필터의 차단 주파수와 노치의
감쇠는 예로 정한 값이다(고역 0.5 Hz, 저역 40 Hz, 노치 60 Hz). 값은 모두 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

setup()
ARTICLE = "fourier-applications"

# 사각파(±1/2, 주기 T)를 RC 저역통과 필터에 넣은 출력
ratios = [0.1, 0.5, 1, 5]  # ω0 RC
fig, axes = plt.subplots(1, 4, figsize=(11, 2.8), sharey=True)
th = np.linspace(0, 2, 1000)  # t / T
for ax, r in zip(axes, ratios):
    x = np.where((th % 1) < 0.5, 0.5, -0.5)
    y = np.zeros_like(th, dtype=complex)
    for k in range(-1999, 2000, 2):
        y += 1 / (1j * np.pi * k) / (1 + 1j * k * r) * np.exp(1j * 2 * np.pi * k * th)
    ax.plot(th, x, color=GRAY, lw=1.2)
    ax.plot(th, y.real, color=BLUE, lw=2)
    ax.set_title(f"$\\omega_0 RC = {r:g}$", loc="left")
    ax.set_xlabel("$t/T$")
    ax.set_ylim(-0.7, 0.7)
axes[0].set_ylabel("전압")
fig.tight_layout()
save(fig, ARTICLE, "rc-square-wave.png")

# 심전도 필터의 크기 응답
f = np.logspace(-2, 2.5, 2000)
s = 2j * np.pi * f
wh, wl, wn = 2 * np.pi * 0.5, 2 * np.pi * 40, 2 * np.pi * 60
hp = s / (s + wh)
lp = wl / (s + wl)
notch = (s**2 + wn**2) / (s**2 + (wn / 5) * s + wn**2)
fig, ax = plt.subplots(figsize=(7, 3.3))
ax.loglog(f, np.abs(hp), color=TEAL, lw=1.3, ls="--", label="고역통과")
ax.loglog(f, np.abs(lp), color=ORANGE, lw=1.3, ls="--", label="저역통과")
ax.loglog(f, np.abs(notch), color=RED, lw=1.3, ls="--", label="노치")
ax.loglog(f, np.abs(hp * lp * notch), color=BLUE, lw=2.2, label="세 필터의 곱")
ax.set_ylim(1e-3, 2)
ax.set_xlabel("주파수 (Hz)")
ax.set_ylabel("$|H(j\\omega)|$")
ax.set_title("심전도 잡음 제거 필터의 크기 응답 (예시 값)", loc="left")
ax.legend(fontsize=9, loc="lower center", ncol=2)
fig.tight_layout()
save(fig, ARTICLE, "ecg-filter.png")

# 회절 예: 강의 자료의 기하
for name, tan_t in [("CD", 1 / 3), ("DVD", 1.0)]:
    t = np.arctan(tan_t)
    print(name, f"theta={t:.3f} sin={np.sin(t):.3f} D={500 / np.sin(t):.0f} nm")
