"""복습 노트의 원식·회로를 직접 계산/작도한다. 원본 그림은 사용하지 않는다."""
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from style import BLUE, TEAL, ORANGE, GRAY, RED, save, setup
setup()

# Normalized one-dimensional diffusion, D=1.
x=np.linspace(-9,9,1201)
fig,axes=plt.subplots(1,2,figsize=(10,3.6))
for t,color in [(0.5,BLUE),(2,TEAL),(8,ORANGE)]:
 p=np.exp(-x*x/(4*t))/math.sqrt(4*math.pi*t)
 axes[0].plot(x,p,color=color,label=f't = {t:g}')
axes[0].set(xlabel='Position x',ylabel='Probability density',title='1D diffusion, D = 1')
axes[0].legend();t=np.linspace(0,8,200)
axes[1].plot(t,2*t,color=BLUE);axes[1].set(xlabel='Time t',ylabel='Mean squared displacement',title=r'$\langle x^2\rangle=2Dt$')
fig.tight_layout();save(fig,'bis223-reference','diffusion.png')

# Contour geometry on positive quadrant.
fig,ax=plt.subplots(figsize=(6.3,4))
u=np.linspace(0,4.3,250);X,Y=np.meshgrid(u,u)
cs=ax.contour(X,Y,X*Y,levels=[1,2,3,4,5,6],colors=GRAY,linewidths=.8)
ax.clabel(cs,fmt='%g');ax.plot([0,4],[4,0],color=BLUE,lw=2,label='x + y = 4')
ax.plot(2,2,'o',color=RED);ax.annotate('(2, 2), xy = 4',(2,2),xytext=(2.3,2.5),arrowprops={'arrowstyle':'-','color':RED})
ax.set(xlim=(0,4.3),ylim=(0,4.3),xlabel='x',ylabel='y',title='Constrained maximum');ax.legend();fig.tight_layout();save(fig,'bis223-reference','lagrange.png')

# Two nondegenerate energy states.
q=np.linspace(0,7,500);pe=1/(1+np.exp(q));pg=1-pe;h=-pe*np.log(pe)-pg*np.log(pg)
fig,axes=plt.subplots(1,2,figsize=(10,3.6))
axes[0].plot(q,pg,color=BLUE,label='Ground');axes[0].plot(q,pe,color=ORANGE,label='Excited');axes[0].legend()
axes[0].set(xlabel=r'$q=\epsilon/(k_BT)$',ylabel='Probability',ylim=(0,1),title='Two-state populations')
axes[1].plot(q,h,color=TEAL);axes[1].axhline(np.log(2),color=GRAY,ls='--',label='ln 2');axes[1].legend();axes[1].set(xlabel=r'$q=\epsilon/(k_BT)$',ylabel=r'$S/k_B$',title='Entropy per two-state system')
fig.tight_layout();save(fig,'bis223-reference','two-state.png')

# SI Debye length for a symmetric 1:1 electrolyte.
eps0=8.8541878128e-12;er=78.5;R=8.31446261815324;T=298.;F=96485.33212331002
fig,axes=plt.subplots(1,2,figsize=(10,3.6));distance=np.linspace(0,30,500)
for molar,color in [(.001,BLUE),(.01,TEAL),(.1,ORANGE)]:
 lam=math.sqrt(eps0*er*R*T/(2*F*F*1000*molar))*1e9
 axes[0].plot(distance,np.exp(-distance/lam),color=color,label=f'{molar*1000:g} mM: {lam:.2f} nm')
axes[0].set(xlabel='Distance (nm)',ylabel=r'$\psi/\psi_0$',title='Planar linearized potential');axes[0].legend()
I=np.logspace(-4,-.3,250);lam=np.sqrt(eps0*er*R*T/(2*F*F*1000*I))*1e9
axes[1].loglog(I,lam,color=BLUE);axes[1].set(xlabel='Ionic strength (mol/L)',ylabel='Debye length (nm)',title='Fixed T and permittivity')
fig.tight_layout();save(fig,'bis223-reference','screening.png')

# Original nodal-analysis circuit schematic, values match text.
fig,ax=plt.subplots(figsize=(8,3.8));ax.set_aspect('equal');ax.axis('off')
def line(x1,y1,x2,y2):ax.plot([x1,x2],[y1,y2],color=BLUE,lw=1.6)
def hr(x1,x2,y,label):
 mid=(x1+x2)/2;line(x1,y,mid-.5,y);line(mid+.5,y,x2,y);ax.add_patch(Rectangle((mid-.5,y-.15),1,.3,fill=False,edgecolor=BLUE,lw=1.6));ax.text(mid,y+.28,label,ha='center')
def vr(x,y1,y2,label):
 mid=(y1+y2)/2;line(x,y1,x,mid-.4);line(x,mid+.4,x,y2);ax.add_patch(Rectangle((x-.15,mid-.4),.3,.8,fill=False,edgecolor=BLUE,lw=1.6));ax.text(x+.23,mid,label,va='center')
line(0,0,6,0);line(0,0,0,1.2);ax.add_patch(Circle((0,1.5),.3,fill=False,edgecolor=BLUE,lw=1.6));line(0,1.8,0,3);ax.text(-.5,1.5,'6 V',ha='right',va='center');ax.text(0,1.59,'+',ha='center',fontsize=9);ax.text(0,1.28,'−',ha='center',fontsize=9)
hr(0,3,3,'2 kΩ');hr(3,6,3,'2 kΩ');vr(3,0,3,'4 kΩ');vr(6,0,3,'2 kΩ')
for xx,name in [(3,'A'),(6,'B')]:ax.plot(xx,3,'o',color=BLUE,ms=5);ax.text(xx,3.38,name,ha='center')
ax.text(3,-.4,'Reference: 0 V',ha='center');ax.set(xlim=(-1,7.1),ylim=(-.6,3.8));fig.tight_layout();save(fig,'circuit-reference','node-example.png')
