"""OCT 문서의 그림.

파장 가변 광원(OFDI)이 파수 k를 선형으로 훑을 때 반사면 두 개에서 생기는 간섭 신호를 만들고,
이를 푸리에 변환해 깊이 방향 반사 분포(A-line)를 되찾는다.
광원의 스펙트럼 포락선은 가우스 모양으로 두었다.
중심 파장, 대역폭, 표본 수, 굴절률, 반사면 위치와 세기는 예로 정한 값이고 모든 값은 직접 계산했다.
"""

import numpy as np
import matplotlib.pyplot as plt

from style import BLUE, GRAY, ORANGE, save, setup

setup()
ARTICLE = "optical-coherence-tomography"

LAM_C = 1.3e-6  # 중심 파장 (m)
D_LAM = 100e-9  # 스펙트럼 포락선의 반치폭 (m)
NS = 2048  # 한 번 훑는 동안의 표본 수
N_TISSUE = 1.35  # 굴절률
SPAN = 3.0  # 훑는 파장 범위 / 반치폭

kc = 2 * np.pi / LAM_C
dk_fwhm = 2 * np.pi * D_LAM / LAM_C**2
k = kc + np.linspace(-0.5, 0.5, NS, endpoint=False) * SPAN * dk_fwhm
dk = k[1] - k[0]
env = np.exp(-4 * np.log(2) * (k - kc) ** 2 / dk_fwhm**2)

reflectors = [(0.5e-3, 1.0), (1.2e-3, 0.4)]  # (깊이, 반사 진폭)
sig = env * sum(r * np.cos(2 * k * N_TISSUE * z) for z, r in reflectors)

pad = 16
spec = np.abs(np.fft.rfft(sig, NS * pad))
z_axis = np.pi * np.arange(spec.size) / (N_TISSUE * NS * pad * dk)
spec /= spec.max()

fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6))
lam_nm = 2 * np.pi / k * 1e9
axes[0].plot(lam_nm, sig, color=BLUE, lw=0.8)
axes[0].plot(lam_nm, env * sum(r for _, r in reflectors), color=GRAY, lw=1, ls="--")
axes[0].set_xlabel("파장 (nm)")
axes[0].set_ylabel("간섭 신호 (상대값)")
axes[0].set_title("파장을 훑는 동안 검출되는 간섭 신호", loc="left")
axes[0].invert_xaxis()

zmax = np.pi / (2 * N_TISSUE * dk)
axes[1].plot(z_axis * 1e3, spec, color=BLUE, lw=1.5)
for z, r in reflectors:
    axes[1].axvline(z * 1e3, color=ORANGE, lw=1, ls="--")
axes[1].set_xlim(0, zmax * 1e3)
axes[1].set_xlabel("깊이 (mm)")
axes[1].set_ylabel("푸리에 변환 크기 (상대값)")
axes[1].set_title("푸리에 변환으로 얻은 깊이 방향 반사 분포", loc="left")
fig.tight_layout()
save(fig, ARTICLE, "ofdi-fringe-aline.png")

dz_formula = 2 * np.log(2) / np.pi * LAM_C**2 / (N_TISSUE * D_LAM)
d_lam_sample = SPAN * D_LAM / NS
range_formula = LAM_C**2 / (4 * N_TISSUE * d_lam_sample)
i0 = int(np.argmin(abs(z_axis - reflectors[0][0])))
half = spec[i0] / 2
lo = i0
while spec[lo] > half:
    lo -= 1
hi = i0
while spec[hi] > half:
    hi += 1
print(f"axial resolution formula {dz_formula*1e6:.2f} um, measured FWHM {(z_axis[hi]-z_axis[lo])*1e6:.2f} um")
print(f"imaging range formula {range_formula*1e3:.2f} mm, FFT Nyquist {zmax*1e3:.2f} mm")
print(f"peak depths {[round(float(z_axis[int(np.argmin(abs(z_axis-z)))]*1e3),3) for z,_ in reflectors]} mm")
print(f"SNR gain Ns/2 = {NS/2:.0f} = {10*np.log10(NS/2):.1f} dB")
print(f"axial resolution in air (n=1) {dz_formula*N_TISSUE*1e6:.2f} um")

# 도플러 위상차 예: A-line 간격 T_A, 빔 방향 속도 v
T_A = 1 / 50e3
kk = 2 * np.pi / LAM_C
for v in (1e-3, 5e-3):
    print(f"Doppler v={v*1e3:g} mm/s: dphi = {2*N_TISSUE*kk*v*T_A:.3f} rad")
print(f"Doppler max unambiguous |v| (dphi=pi): {np.pi/(2*N_TISSUE*kk*T_A)*1e3:.1f} mm/s")
