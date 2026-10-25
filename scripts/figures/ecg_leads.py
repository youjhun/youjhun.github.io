"""ECG 측정 원리 문서의 그림: 전두면 사지 유도의 방향(육축 체계).

각 유도의 양의 방향을 표준 각도로 그린다: I 0°, II +60°, III +120°, aVL −30°, aVF +90°,
aVR −150°. 각도는 아래쪽을 +로 재는 ECG 관례를 따른다.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, save, setup

setup()
leads = [("I", 0, BLUE), ("II", 60, BLUE), ("III", 120, BLUE),
         ("aVL", -30, ORANGE), ("aVF", 90, ORANGE), ("aVR", -150, ORANGE)]
fig, ax = plt.subplots(figsize=(4.4, 4.4))
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(th), np.sin(th), color=GRAY, lw=0.8, ls=":")
for name, deg, c in leads:
    a = np.radians(deg)
    x, y = np.cos(a), -np.sin(a)  # 아래쪽이 +
    ax.annotate("", xy=(x, y), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=c, lw=1.8))
    ax.plot([0, -x], [0, -y], color=c, lw=0.8, ls="--")
    ax.text(1.17 * x, 1.17 * y, f"{name}\n{deg:+d}°" if deg else f"{name}\n0°", ha="center", va="center", fontsize=9.5, color=c)
ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.45, 1.45)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("전두면 사지 유도의 양의 방향", loc="left")
fig.tight_layout()
save(fig, "ecg", "limb-lead-axes.png")
