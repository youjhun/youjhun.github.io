"""센서 네트워크의 깨어남 일정과 시간 동기화 문서의 그림.

듀티 사이클 네트워크에서 패킷이 싱크까지 가는 데 걸리는 평균 시간을 단순 모형으로 계산한다.

- 같은 시각에 깨어나는 동기식: 한 주기에 한 홉만 전달된다.
- 파이프라인 일정: 깊이마다 슬롯 하나씩 어긋나게 깨어나 한 주기 안에 여러 홉을 지난다.
- 링크가 확률 p로 실패하면 단일 파이프라인은 다음 주기까지 기다리고,
  부모가 둘인 파이프라인은 다음 슬롯의 두 번째 부모에게 한 번 더 보낸다.

패킷은 주기 안의 임의 시각에 생긴다고 보고 첫 깨어남까지 평균 T/2를 기다린다.
주기, 슬롯 길이, 홉 수는 예로 정한 값이고, 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, ORANGE, TEAL, save, setup

setup()
ARTICLE = "wakeup-scheduling-time-sync"

T = 10.0  # 동작 주기 (s)
S = 0.02  # 슬롯 길이 (s)


def lat_sync(h):
    return T / 2 + (h - 1) * T + S


def lat_pipe(h):
    return T / 2 + h * S


def hop_single(p):
    # 성공할 때까지 주기마다 한 번 시도한다
    return S + p / (1 - p) * T


def hop_two(p):
    # 첫 부모 실패 시 다음 슬롯의 두 번째 부모, 둘 다 실패하면 다음 주기
    q = 1 - p * p
    return ((1 - p) * S + p * (1 - p) * 2 * S) / q + p * p / q * T


fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))

h = np.arange(1, 21)
axes[0].semilogy(h, lat_sync(h), "o-", color=ORANGE, lw=2, ms=4, label="같은 시각에 깨어남")
axes[0].semilogy(h, lat_pipe(h), "o-", color=BLUE, lw=2, ms=4, label="파이프라인 일정")
axes[0].set_xlabel("싱크까지의 홉 수")
axes[0].set_ylabel("평균 전달 시간 (s)")
axes[0].set_title("홉 수에 따른 평균 전달 시간", loc="left")
axes[0].set_xticks([1, 5, 10, 15, 20])
axes[0].legend(fontsize=9)

H = 10
p = np.linspace(0, 0.5, 201)
axes[1].plot(p * 100, T / 2 + H * hop_single(p), color=ORANGE, lw=2, label="단일 파이프라인")
axes[1].plot(p * 100, T / 2 + H * hop_two(p), color=TEAL, lw=2, label="부모 둘인 파이프라인")
axes[1].axhline(lat_sync(H), color=BLUE, lw=1, ls="--", label="같은 시각에 깨어남, 손실 없음")
axes[1].set_xlabel("링크 실패 확률 (%)")
axes[1].set_ylabel("평균 전달 시간 (s)")
axes[1].set_title("10홉 경로에서 링크 실패 확률과 평균 전달 시간", loc="left")
axes[1].legend(fontsize=9)
fig.tight_layout()
save(fig, ARTICLE, "pipeline-latency.png")

for hh in (1, 5, 10):
    print(f"H={hh}: sync {lat_sync(hh):.2f}s, pipeline {lat_pipe(hh):.2f}s")
for pp in (0.1, 0.2, 0.3):
    print(f"p={pp}: single {T/2 + H*hop_single(pp):.2f}s, two parents {T/2 + H*hop_two(pp):.2f}s")


def tpsn(offset, d_up, d_down, t1=100.0, hold=0.004):
    t2 = t1 + d_up + offset
    t3 = t2 + hold
    t4 = t3 - offset + d_down
    d = ((t2 - t1) + (t4 - t3)) / 2
    delta = ((t2 - t1) - (t4 - t3)) / 2
    return t2, t3, t4, d, delta


for up, down in ((1e-3, 1e-3), (1e-3, 3e-3)):
    t2, t3, t4, d, delta = tpsn(5e-3, up, down)
    print(f"TPSN up={up*1e3:g}ms down={down*1e3:g}ms: T2={t2:.3f} T3={t3:.3f} T4={t4:.3f} d={d*1e3:.2f}ms delta={delta*1e3:.2f}ms")
