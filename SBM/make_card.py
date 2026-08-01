"""Open Graph card, 1200x630. Background is a real Chladni nodal set (m=3,n=5):
   grains random-walk with step proportional to |u| and drift down grad(u^2),
   so they settle exactly on u = 0."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng=np.random.default_rng(11)
m,n=3,5; N=200000; PI=np.pi
x=rng.random(N); y=rng.random(N)
cx,cy=PI*n,PI*m
def chi(x,y): return np.cos(cx*x)*np.cos(cy*y)-np.cos(cy*x)*np.cos(cx*y)
for i in range(230):
    v=chi(x,y); a=np.abs(v)/2.0
    dx=-cx*np.sin(cx*x)*np.cos(cy*y)+cy*np.sin(cy*x)*np.cos(cx*y)
    dy=-cy*np.cos(cx*x)*np.sin(cy*y)+cx*np.cos(cy*x)*np.sin(cx*y)
    x-=0.00175*v*dx; y-=0.00175*v*dy
    s=0.013*a
    x+=(rng.random(N)-.5)*s; y+=(rng.random(N)-.5)*s
    x=np.abs(x); x=np.where(x>1,2-x,x)
    y=np.abs(y); y=np.where(y>1,2-y,y)

fig=plt.figure(figsize=(12,6.3),dpi=100)
fig.patch.set_facecolor("#0a0a0c")
ax=fig.add_axes([0,0,1,1]); ax.set_facecolor("#0a0a0c"); ax.axis("off")
ax.set_xlim(0,1); ax.set_ylim(0,1)
# plate occupies the left 42%, square, vertically centred
PW=0.40; x0=0.015; y0=0.06; PH=0.88
ax.scatter(x0+x*PW, y0+y*PH, s=0.35, c="#f2e8d5", alpha=0.42, marker=".", linewidths=0)
ax.add_patch(plt.Rectangle((x0,y0),PW,PH,fill=False,ec="#2a2a34",lw=1.2,zorder=2))

TX=0.485
def T(yy,txt,size,color,**kw):
    ax.text(TX,yy,txt,color=color,fontsize=size,transform=ax.transAxes,zorder=3,
            va="top",**kw)
T(0.925,"XII BIENAL DA SBM · 2026",19,"#d4a24c",family="monospace",fontweight="bold")
T(0.815,"Cimática, Atratores\ne a Escada\nde Recorrência",37,"#e8e8ef",
  family="serif",fontweight="bold",linespacing=1.16)
T(0.375,"Pablo Nogueira Grossi · G6 LLC",21,"#e8e8ef",family="serif")
T(0.300,"UFRN · Natal-RN · 3–7 de agosto de 2026",18,"#8a8a96",family="serif")
xx=TX
for c,col in [("EXP13","#7aa2c8"),("MC48","#d4a24c"),("CO144","#d4a24c"),
              ("P290","#d4a24c"),("OF53","#d4a24c")]:
    ax.text(xx,0.155,c,color=col,fontsize=16,family="monospace",fontweight="bold",
            transform=ax.transAxes,zorder=3,va="top")
    xx+=0.052+0.0125*len(c)
T(0.085,"exposição · minicurso · comunicação · pôster · oficina",14.5,"#5e5e6a",family="serif")
fig.savefig("card.png",facecolor="#0a0a0c")
print("card.png written")
