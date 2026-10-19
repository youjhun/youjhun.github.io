"""양자화와 ADC 문서의 그림."""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, LIGHT, ORANGE, RED, TEAL, save, setup

ARTICLE = "quantization-adc"
setup()


def quantize(x, bits, full_scale=1.0):
    """[-full_scale, full_scale] 범위의 mid-rise 균일 양자화.

    출력 단계는 ±Δ/2, ±3Δ/2, …, ±(full_scale − Δ/2)의 2^bits개다. 범위 안의 입력은 오차가 언제나
    Δ/2 이하이므로, 6.02N + 1.76 dB가 가정하는 '잘리지 않은 꽉 찬 사인파'와 조건이 맞는다.
    """
    delta = 2 * full_scale / 2**bits
    q = (np.floor(x / delta) + 0.5) * delta
    return np.clip(q, -full_scale + delta / 2, full_scale - delta / 2), delta


# 그림 1. 계단 모양의 입출력 관계와 그 오차
x = np.linspace(-1, 1, 4000)
q, delta = quantize(x, 3)
fig, axes = plt.subplots(2, 1, figsize=(7.5, 5.6), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
axes[0].plot(x, x, color=GRAY, ls="--", lw=1, label="이상적인 출력 (입력 그대로)")
axes[0].plot(x, q, color=BLUE, lw=2, label="3비트 양자화 출력 (8단계)")
axes[0].set_ylabel("출력")
axes[0].legend(loc="upper left", fontsize=9.5)
axes[0].set_title("3비트 ADC: 연속 입력을 8개 값 중 하나로 반올림한다")
axes[1].plot(x, q - x, color=RED, lw=1.4)
axes[1].axhline(delta / 2, color=ORANGE, ls=":", lw=1)
axes[1].axhline(-delta / 2, color=ORANGE, ls=":", lw=1)
axes[1].text(-0.98, delta / 2 + 0.02, "+Δ/2", color=ORANGE)
axes[1].text(-0.98, -delta / 2 - 0.09, "−Δ/2", color=ORANGE)
axes[1].set_ylabel("오차")
axes[1].set_xlabel("입력 (최대 범위로 정규화)")
fig.tight_layout()
save(fig, ARTICLE, "staircase.png")

# 그림 2. 오차가 잡음처럼 보이는 조건: 비트가 적고 신호가 느리면 오차는 신호를 따라가는 왜곡이다
t = np.linspace(0, 1, 2000)
slow = 0.95 * np.sin(2 * np.pi * 2 * t)
busy = 0.8 * np.sin(2 * np.pi * 2 * t) + 0.15 * np.sin(2 * np.pi * 37 * t + 0.4)
fig, axes = plt.subplots(2, 2, figsize=(10, 4.8), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
for col, (sig, bits, title) in enumerate([
    (slow, 3, "3비트, 느린 사인파: 오차가 신호를 따라간다"),
    (busy, 8, "8비트, 빠른 성분이 섞인 신호: 오차가 잡음처럼 보인다"),
]):
    q, d = quantize(sig, bits)
    axes[0, col].plot(t, sig, color=GRAY, lw=1.4, label="원래 신호")
    axes[0, col].plot(t, q, color=BLUE, lw=1.4 if bits == 3 else 0.9, label=f"{bits}비트 양자화")
    axes[0, col].set_title(title, fontsize=10.5, loc="left")
    axes[0, col].legend(loc="upper right", fontsize=8.5)
    axes[1, col].plot(t, (q - sig) / d, color=RED, lw=0.8)
    axes[1, col].set_ylim(-0.6, 0.6)
    axes[1, col].set_xlabel("시간 (s)")
axes[1, 0].set_ylabel("오차 / Δ")
fig.tight_layout()
save(fig, ARTICLE, "sine.png")

# 그림 3. 비트 하나에 약 6 dB. 범위를 덜 쓰면 그만큼 잃는다
rng = np.random.default_rng(0)
bits = np.arange(4, 17)
n = np.arange(200000)
f = 0.01234567  # 표본 주기와 맞물리지 않는 주파수
phase = rng.uniform(0, 2 * np.pi)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(bits, 6.02 * bits + 1.76, color=GRAY, lw=1.5, label="이론: 6.02N + 1.76 dB")
for amp_db, color, label in [(0, BLUE, "꽉 찬 사인파 (0 dBFS)"), (-20, ORANGE, "범위의 1/10만 쓰는 사인파 (−20 dBFS)")]:
    A = 10 ** (amp_db / 20)
    sig = A * np.sin(2 * np.pi * f * n + phase)
    snr = []
    for b in bits:
        qq, _ = quantize(sig, b)
        snr.append(10 * np.log10(np.mean(sig**2) / np.mean((qq - sig) ** 2)))
    ax.plot(bits, snr, "o", color=color, label=f"시뮬레이션: {label}")
ax.set_xlabel("비트 수 N")
ax.set_ylabel("신호 대 양자화 잡음비 (dB)")
ax.set_title("비트 하나를 늘리면 약 6 dB 좋아진다")
ax.legend(fontsize=9.5)
save(fig, ARTICLE, "sqnr.png")
