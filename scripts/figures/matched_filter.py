"""정합 필터 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from gold import LENGTH, gold, periodic_xcorr
from style import BLUE, GRAY, ORANGE, RED, TEAL, save, setup

ARTICLE = "matched-filter"
setup()
rng = np.random.default_rng(7)

# 그림 1. 잡음에 묻힌 펄스를 정합 필터가 찾아낸다
s = gold(3).astype(float)
N = 400
delay = 150
r = np.random.default_rng(3).normal(0, 1.0, N)
r[delay : delay + LENGTH] += s
out = np.correlate(r, s, mode="valid")  # out[k] = Σ r[k+i]·s[i]
thr = 4 * np.sqrt(np.mean(out**2))

fig, axes = plt.subplots(3, 1, figsize=(8.5, 6.4))
axes[0].step(np.arange(LENGTH + 1), np.r_[s, s[-1]], where="post", color=BLUE, lw=1.6)
axes[0].set_title("(가) 찾을 모양 s[n]: 길이 31의 ±1 부호", loc="left")
axes[0].set_yticks([-1, 1])
axes[0].set_xlim(0, LENGTH)
axes[1].plot(r, color=GRAY, lw=0.9)
axes[1].axvspan(delay, delay + LENGTH, color=ORANGE, alpha=0.15)
axes[1].text(delay + LENGTH / 2, 3.4, "여기에 s가 숨어 있다", color=ORANGE, ha="center")
axes[1].set_title("(나) 받은 신호 r[n] = s[n − 150] + 잡음: 눈으로는 어디 있는지 모른다", loc="left")
axes[1].set_ylim(-4.2, 4.2)
axes[2].plot(out, color=BLUE, lw=1.3)
axes[2].axhline(thr, color=RED, ls="--", lw=1.1)
axes[2].text(len(out) - 2, thr + 2, "문턱값", color=RED, ha="right")
peak = int(np.argmax(out))
axes[2].plot(peak, out[peak], "o", color=RED, ms=7)
axes[2].annotate(f"n = {peak}에서 최대", (peak, out[peak]), (peak + 40, out[peak] - 6), color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED))
axes[2].set_title("(다) 정합 필터 출력: s가 시작한 자리에서 뾰족하게 솟는다", loc="left")
axes[2].set_xlabel("n (표본)")
for ax in axes[1:]:
    ax.set_xlim(0, N)
fig.tight_layout()
save(fig, ARTICLE, "detect.png")

# 그림 2. Gold code의 자기상관과 상호상관
a, b = gold(3), gold(11)
lags = np.arange(LENGTH)
ac, cc = periodic_xcorr(a, a), periodic_xcorr(a, b)
fig, axes = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)
for ax, c, title, color in [
    (axes[0], ac, "자기상관: 제 부호와 맞추면", BLUE),
    (axes[1], cc, "상호상관: 남의 부호와 맞추면", TEAL),
]:
    ax.vlines(lags, 0, c, color=color, lw=1.4)
    ax.plot(lags, c, "o", color=color, ms=4)
    ax.axhline(0, color="#777", lw=0.7)
    ax.set_title(title)
    ax.set_xlabel("어긋난 칸 수")
axes[0].set_ylabel("상관값")
axes[0].annotate("31 (정렬됐을 때)", (0, 31), (6, 27), color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE))
axes[1].text(15, 20, "어디서든 −9, −1, 7 중 하나", color=TEAL, ha="center")
axes[0].set_ylim(-13, 35)
fig.tight_layout()
save(fig, ARTICLE, "gold-correlation.png")

# 그림 3. 두 노드의 신호가 겹쳐도 각자의 필터는 제 노드만 찾는다
sa, sb = gold(3).astype(float), gold(11).astype(float)
N = 240
r = rng.normal(0, 0.8, N)
ta, tb = 90, 104
r[ta : ta + LENGTH] += sa
r[tb : tb + LENGTH] += sb
oa = np.correlate(r, sa, mode="valid")
ob = np.correlate(r, sb, mode="valid")
fig, axes = plt.subplots(3, 1, figsize=(8.5, 6), sharex=True)
axes[0].plot(r, color=GRAY, lw=0.9)
axes[0].axvspan(ta, ta + LENGTH, color=BLUE, alpha=0.12)
axes[0].axvspan(tb, tb + LENGTH, color=TEAL, alpha=0.12)
axes[0].set_title("받은 신호: 노드 A(n = 90)와 노드 B(n = 104)가 겹쳐 들어왔다", loc="left")
axes[1].plot(oa, color=BLUE, lw=1.3)
axes[1].axvline(ta, color=BLUE, ls=":", lw=1)
axes[1].set_title("A의 부호로 만든 정합 필터 → A의 자리에서만 솟는다", loc="left")
axes[2].plot(ob, color=TEAL, lw=1.3)
axes[2].axvline(tb, color=TEAL, ls=":", lw=1)
axes[2].set_title("B의 부호로 만든 정합 필터 → B의 자리에서만 솟는다", loc="left")
axes[2].set_xlabel("n (표본)")
axes[2].set_xlim(0, N)
fig.tight_layout()
save(fig, ARTICLE, "separation.png")
