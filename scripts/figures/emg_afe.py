"""EMG AFE figures: theory and reported summary values, not SPICE waveforms.

Run from repository root: python3 scripts/figures/emg_afe.py
Raw output CSVs were not available. No plot here impersonates measured output.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
from style import setup, save, BLUE, TEAL, RED, ORANGE, GRAY, LIGHT

setup()
# Keep common styling; append a CJK fallback when the site's fonts are absent.
available = {f.name for f in font_manager.fontManager.ttflist}
if not ({'Pretendard', 'NanumGothic'} & available):
    plt.rcParams['font.family'] = ['Noto Sans CJK JP', 'DejaVu Sans']
ARTICLE = 'emg-afe-kicad'

fig, ax = plt.subplots(figsize=(12,7.8))
ax.set(xlim=(-.4,9.9),ylim=(-1.4,7.7)); ax.axis('off')
blocks = [
    ('U2 · 차동 증폭','INA333 / R4 10 kΩ\nG₁ = 11 / EMG_PRE'),
    ('C1 · R5 · HPF','100 nF / 100 kΩ → VBIAS\nfc ≈ 15.9 Hz / EMG_HP'),
    ('U3 · 추가 증폭','R7 100 kΩ / R6 1 kΩ\nG₂ = 101 / EMG_AMP'),
    ('R8 · C2 · LPF','3.3 kΩ / 100 nF → GND\nfc ≈ 482 Hz / EMG_LPF'),
    ('U4 · D1 · 반파 정류','피드백: 다이오드 뒤\nR9 → VBIAS / EMG_RECT'),
    ('U5 · 정류 버퍼','+ ← EMG_RECT\n출력 → − 및 R10'),
    ('R10 · C3 · 평활','47 kΩ / 1 µF → GND\nτ = 47 ms / EMG_ENV'),
    ('U7 · 포락선 버퍼','+ ← EMG_ENV\n출력 → − / EMG_ENV_BUF'),
    ('U6 · 히스테리시스','R11 1 kΩ / R12 3.3 MΩ\nV4 = 1.642 V / ACTIVITY'),
]
positions=[]
for i,(title,body) in enumerate(blocks):
    row,col=divmod(i,3); x=col*3.25; y=5.5-row*2.4
    positions.append((x,y))
    box=FancyBboxPatch((x,y),2.75,1.6,boxstyle='round,pad=0.08',fc=LIGHT,ec=BLUE,lw=1.2)
    ax.add_patch(box)
    ax.text(x+1.375,y+1.18,title,ha='center',va='center',color=BLUE,fontsize=11,fontweight='bold')
    ax.text(x+1.375,y+.56,body,ha='center',va='center',fontsize=10)
    if col:
        ax.annotate('',xy=(x-.1,y+.8),xytext=(x-.5,y+.8),arrowprops={'arrowstyle':'->','color':BLUE,'lw':1.5})
for row in [0,1]:
    x,y=positions[row*3+2]; xnext,ynext=positions[(row+1)*3]
    ax.plot([x+2.75,9.6,9.6,-.25,-.25],[y+.8,y+.8,y-.32,y-.32,ynext+.8],color=GRAY,lw=1)
    ax.annotate('',xy=(xnext-.08,ynext+.8),xytext=(-.25,ynext+.8),arrowprops={'arrowstyle':'->','color':GRAY})
ax.text(4.5,7.55,'EMG 증폭·필터·활동 판정',ha='center',fontsize=16,color=BLUE)
ax.text(4.5,-.78,'U1: 100 kΩ / 100 kΩ 분압 → 버퍼 → VBIAS ≈ 1.64 V\nVBIAS 연결: U2 REF · R5 · R6 · R9    |    모든 OPAMP 전원: 3.3 V / GND',ha='center',fontsize=11,color=BLUE)
ax.text(4.5,-1.32,'회로도 화면을 참고한 기능도 · 배선 검증용 넷리스트가 아님 · 이전 C3 = 2 µF 조건은 τ = 94 ms',ha='center',fontsize=9,color='#555555')
save(fig,ARTICLE,'circuit-overview.png')

# Illustrative half-wave rectification and RC smoothing, initialized at VBIAS.
dt=1e-5; t=np.arange(0,1.200001,dt); bias=1.64
amplitude=np.where((t>=.35)&(t<.8),.45,.08)
x=amplitude*np.sin(2*np.pi*1000*t)
rect=bias+np.maximum(x,0)
y=np.empty_like(t); y[0]=bias; alpha=np.exp(-dt/.047)
for i in range(1,len(t)):
    y[i]=alpha*y[i-1]+(1-alpha)*rect[i]
fig,axes=plt.subplots(3,1,figsize=(10,7.2),sharex=True)
for ax,signal,color in zip(axes,[bias+x,rect,y],[BLUE,ORANGE,TEAL]):
    ax.plot(t,signal,color=color,lw=.55)
    ax.axhline(bias,color=GRAY,lw=.8,ls='--'); ax.set_ylabel('전압 (V)')
axes[0].set_title('가상 1 kHz 입력 · 진폭 0.08 → 0.45 → 0.08 V',loc='left')
axes[1].set_title('VBIAS 기준의 이상적 반파 정류',loc='left')
axes[2].set_title('RC 평활 · τ = 47 ms',loc='left'); axes[2].set_xlabel('시간 (s)')
axes[2].plot(t,bias+amplitude/np.pi,color=GRAY,lw=1,ls=':',label='진폭 / π + VBIAS')
axes[2].legend(loc='lower right')
fig.text(.1,.015,'계산 예 · KiCad 출력 및 GRABMyo 재생 결과가 아님 · 초기값은 VBIAS로 설정',fontsize=9,color='#555555')
fig.tight_layout(rect=(0,.04,1,1)); save(fig,ARTICLE,'rectify-smooth.png')

ranges=[(1.63980,1.64027,1.64100),(1.64292,1.64949,1.67007)]
ron=1.642+1/3300*1.642; roff=1.642+1/3300*(1.642-3.3)
fig,axes=plt.subplots(1,2,figsize=(11,3.9),sharey=True,gridspec_kw={'width_ratios':[1.35,1]})
for ax in axes:
    for row,((lo,mean,hi),color) in enumerate(zip(ranges,[BLUE,TEAL])):
        ax.plot([lo,hi],[row,row],lw=7,solid_capstyle='butt',color=color,alpha=.65)
        ax.scatter([mean],[row],s=45,color=color,zorder=3)
    ax.axvline(ron,color=RED,ls='--',lw=1.3,label='ON 1.642498 V')
    ax.axvline(roff,color=ORANGE,ls=':',lw=1.5,label='OFF 1.641498 V')
    ax.set_yticks([0,1],['휴식','주먹']); ax.set_ylim(-.6,1.6); ax.set_xlabel('EMG_ENV_BUF (V)')
axes[0].set_xlim(1.6385,1.672); axes[0].set_title('보고된 MIN–MAX · 점은 AVG',loc='left')
axes[1].set_xlim(1.6403,1.6434); axes[1].set_title('두 범위 사이의 확대',loc='left'); axes[1].tick_params(labelbottom=True)
axes[0].legend(loc='upper right',fontsize=9)
fig.text(.1,.015,'측정 요약값의 재표현 · 오차막대/신뢰구간이 아님 · 계산 문턱은 출력 0–3.3 V 가정',fontsize=9,color='#555555')
fig.tight_layout(rect=(0,.06,1,1)); save(fig,ARTICLE,'threshold-ranges.png')

fig,ax=plt.subplots(figsize=(10,2.8))
for lo,hi,label,color in [(0,.5,'REST',BLUE),(.5,2.5,'HAND CLOSE',TEAL),(2.5,5,'REST',BLUE)]:
    ax.axvspan(lo,hi,color=color,alpha=.16)
    ax.text((lo+hi)/2,.55,label,ha='center',va='center',color=color,fontsize=12)
for edge in [.5,2.5]: ax.axvline(edge,color=GRAY,ls='--',lw=1)
ax.set(xlim=(0,5),ylim=(0,1),yticks=[],xlabel='시뮬레이션 시간 (s)',title='BSELECT의 입력 선택 구간')
fig.text(.1,.015,'출력 파형이 아닌 입력 일정 · 두 기록은 시간 0부터 동시에 진행 · 생리학적 onset 라벨이 아님',fontsize=9,color='#555555')
fig.tight_layout(rect=(0,.08,1,1)); save(fig,ARTICLE,'transition-schedule.png')

f=np.geomspace(.1,1e4,1000)
hp=(1j*2*np.pi*f*.01)/(1+1j*2*np.pi*f*.01)
lp=1/(1+1j*2*np.pi*f*.00033)
fig,axes=plt.subplots(2,1,figsize=(9,6),sharex=True)
for h,label,color in [(hp,'HPF: 100 kΩ / 100 nF',BLUE),(lp,'LPF: 3.3 kΩ / 100 nF',TEAL),(hp*lp,'HPF × LPF',ORANGE)]:
    axes[0].semilogx(f,20*np.log10(abs(h)),label=label,color=color)
    axes[1].semilogx(f,np.angle(h,deg=True),color=color)
axes[0].set(ylabel='크기 (dB)',ylim=(-45,3),title='부하를 무시한 두 RC 필터의 계산 응답'); axes[0].legend()
axes[1].set(ylabel='위상 (°)',xlabel='주파수 (Hz)',ylim=(-95,95))
fig.tight_layout(); save(fig,ARTICLE,'filter-response.png')
