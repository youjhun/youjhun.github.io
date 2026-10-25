"""MIT HST.582J 블라인드 신호 분리 문서의 그림.

두 원천(사인파와 라플라스 분포 잡음)을 2×2 행렬로 섞은 뒤, PCA로 whitening하고
첨도의 절댓값 합이 가장 큰 회전을 찾아 분리한다. 2차원이라 회전각을 격자로 훑는다.
원천, 혼합 행렬, 표본 수는 예로 정한 값이고 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, TEAL, save, setup

setup()
ARTICLE = "blind-source-separation"
rng = np.random.default_rng(0)
M = 2000
t = np.arange(M)
s = np.vstack([np.sqrt(2) * np.sin(2 * np.pi * t / 97.0), rng.laplace(0, 1 / np.sqrt(2), M)])
A = np.array([[1.0, 0.6], [0.4, 1.0]])
x = A @ s


def kurt(v):
    v = (v - v.mean()) / v.std()
    return np.mean(v**4) - 3


# PCA whitening
xc = x - x.mean(axis=1, keepdims=True)
C = xc @ xc.T / M
d, E = np.linalg.eigh(C)
V = np.diag(1 / np.sqrt(d)) @ E.T
w = V @ xc

angles = np.linspace(0, np.pi / 2, 901)
score = []
for a in angles:
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    y = R @ w
    score.append(abs(kurt(y[0])) + abs(kurt(y[1])))
a_best = angles[int(np.argmax(score))]
R = np.array([[np.cos(a_best), -np.sin(a_best)], [np.sin(a_best), np.cos(a_best)]])
y = R @ w

fig, axes = plt.subplots(1, 4, figsize=(11.5, 3.1))
panels = [(s, "원천 $s$"), (x, "혼합 $x = As$"), (w, "whitening"), (y, "첨도 최대화 회전")]
for ax, (v, name) in zip(axes, panels):
    ax.plot(v[0], v[1], ".", color=BLUE, ms=1.5, alpha=0.5)
    ax.set_title(name, loc="left")
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
save(fig, ARTICLE, "ica-scatter.png")

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(np.degrees(angles), score, color=TEAL, lw=2)
ax.axvline(np.degrees(a_best), color=GRAY, ls="--", lw=1)
ax.set_xlabel("회전각 (도)")
ax.set_ylabel("$|\\kappa_1 - 3| + |\\kappa_2 - 3|$")
ax.set_title("whitening한 신호의 회전각에 따른 초과 첨도 절댓값 합", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "kurtosis-vs-angle.png")

print("excess kurtosis sources:", [round(float(kurt(r)), 2) for r in s])
print("excess kurtosis mixtures:", [round(float(kurt(r)), 2) for r in x])
print("excess kurtosis whitened:", [round(float(kurt(r)), 2) for r in w])
print("excess kurtosis ICA:", [round(float(kurt(r)), 2) for r in y], "best angle", round(float(np.degrees(a_best)), 1))
cc = np.corrcoef(np.vstack([s, y]))[:2, 2:]
print("|corr(source, estimate)|:\n", np.round(np.abs(cc), 3))
