"""저전력 센서 네트워크 MAC 문서의 그림.

송신 노드 하나와 수신 노드 하나로 이루어진 쌍의 평균 전력을 단순 모형으로 계산한다.

- 저전력 청취(B-MAC 방식): 수신기가 주기 T마다 t_s 동안 채널을 확인하고,
  송신기는 패킷마다 길이 T의 프리앰블을 보낸다. 수신기는 평균 T/2 동안 프리앰블을 듣는다.
- 짧은 프리앰블 열(X-MAC 방식): 수신기가 깨어나면 바로 응답하므로 송신기는 평균 T/2만 보낸다.
- 웨이크업 라디오: 수신기의 초저전력 라디오가 늘 켜져 있고, 패킷마다 짧은 깨우기 신호를 보낸다.

동기화 비용, 충돌, 엿듣기, 잠자는 동안의 전력은 넣지 않았다.
전력과 시간 값은 예로 정한 것이고, 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import brentq

from style import BLUE, ORANGE, TEAL, save, setup

setup()
ARTICLE = "low-power-mac"

P_RADIO = 60e-3  # 주 라디오의 송수신 전력 (W)
T_S = 2.5e-3  # 채널 확인 시간 (s)
E_DATA = P_RADIO * 4e-3 * 2  # 데이터와 ACK를 합친 4 ms 동안 두 노드가 쓰는 에너지 (J)
E_WAKE = P_RADIO * 1e-3  # 깨우기 신호 한 번의 에너지 (J)


def p_bmac(T, lam):
    return P_RADIO * T_S / T + lam * (P_RADIO * T + P_RADIO * T / 2 + E_DATA)


def p_xmac(T, lam):
    return P_RADIO * T_S / T + lam * (P_RADIO * T / 2 + E_DATA)



def p_wur(lam, p_ulp):
    return p_ulp + lam * (E_WAKE + E_DATA)


fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))

T = np.logspace(-2, 2, 400)
lam = 1 / 60
for f, name, c in [(p_bmac, "긴 프리앰블(B-MAC 방식)", ORANGE), (p_xmac, "짧은 프리앰블 열(X-MAC 방식)", BLUE)]:
    p = f(T, lam)
    axes[0].loglog(T, p * 1e6, color=c, lw=2, label=name)
    i = np.argmin(p)
    axes[0].plot(T[i], p[i] * 1e6, "o", color=c)
axes[0].set_xlabel("채널 확인 주기 $T$ (s)")
axes[0].set_ylabel("평균 전력 (µW)")
axes[0].set_title("분당 패킷 1개일 때 확인 주기와 평균 전력", loc="left")
axes[0].legend(fontsize=9)

lams = np.logspace(-7, 0, 400)
T_b = np.sqrt(T_S / (lams * 1.5))
T_x = np.sqrt(T_S / (lams * 0.5))
axes[1].loglog(lams, p_bmac(T_b, lams) * 1e6, color=ORANGE, lw=2, label="긴 프리앰블, 최적 $T$")
axes[1].loglog(lams, p_xmac(T_x, lams) * 1e6, color=BLUE, lw=2, label="짧은 프리앰블 열, 최적 $T$")
axes[1].loglog(lams, p_wur(lams, 50e-6) * 1e6, color=TEAL, lw=2, label="웨이크업 라디오 50 µW")
axes[1].loglog(lams, p_wur(lams, 5e-6) * 1e6, color=TEAL, lw=2, ls="--", label="웨이크업 라디오 5 µW")
axes[1].set_xlabel("패킷 발생률 (패킷/s)")
axes[1].set_ylabel("평균 전력 (µW)")
axes[1].set_title("패킷 발생률에 따른 평균 전력", loc="left")
axes[1].legend(fontsize=9)
fig.tight_layout()
save(fig, ARTICLE, "duty-cycle-energy.png")

i_b = np.argmin(p_bmac(T, lam))
i_x = np.argmin(p_xmac(T, lam))
print(f"lam=1/60: B-MAC T*={T[i_b]:.3f}s P={p_bmac(T[i_b], lam)*1e6:.0f}uW; X-MAC T*={T[i_x]:.3f}s P={p_xmac(T[i_x], lam)*1e6:.0f}uW")
print(f"always-on receive: {P_RADIO*1e3:.0f} mW")
for p_ulp in (50e-6, 5e-6):
    cb = brentq(lambda l: p_bmac(np.sqrt(T_S / (l * 1.5)), l) - p_wur(l, p_ulp), 1e-9, 1)
    cx = brentq(lambda l: p_xmac(np.sqrt(T_S / (l * 0.5)), l) - p_wur(l, p_ulp), 1e-9, 1)
    print(f"ulp={p_ulp*1e6:g}uW crossover B-MAC lam={cb:.2e} (1 per {1/cb/3600:.2f} h), X-MAC lam={cx:.2e} (1 per {1/cx/3600:.2f} h)")
for l in (1e-4, 1e-2, 1):
    print(f"lam={l:g}: B {p_bmac(np.sqrt(T_S/(l*1.5)), l)*1e6:.1f}uW T*={np.sqrt(T_S/(l*1.5)):.2f}s; X {p_xmac(np.sqrt(T_S/(l*0.5)), l)*1e6:.1f}uW T*={np.sqrt(T_S/(l*0.5)):.2f}s; WuR50 {p_wur(l,50e-6)*1e6:.1f}uW; WuR5 {p_wur(l,5e-6)*1e6:.1f}")
