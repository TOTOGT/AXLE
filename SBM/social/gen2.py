import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
SAND="#f4ecdb"; PLATE="#0b0b0e"; GOLD="#d4a24c"; DIM="#9a9aa6"
PI=np.pi; G=1400

cmap=LinearSegmentedColormap.from_list("sand",[(0,PLATE),(0.35,"#3a3428"),(1,SAND)])

def besselJ(k,x):
    x=np.asarray(x,dtype=float); h=x/2.0
    term=np.ones_like(x)
    for i in range(1,k+1): term*=h/i
    s=term.copy()
    for i in range(1,70):
        term=term*(-(h*h)/(i*(i+k))); s=s+term
    return s
def jzero(k,s):
    x=k+1.0; prev=besselJ(k,np.array([x]))[0]; out=[]
    while len(out)<s and x<200:
        nx=x+0.02; cv=besselJ(k,np.array([nx]))[0]
        if (prev<0)!=(cv<0):
            lo,hi=x,nx
            for _ in range(60):
                m=(lo+hi)/2
                if (besselJ(k,np.array([lo]))[0]<0)!=(besselJ(k,np.array([m]))[0]<0): hi=m
                else: lo=m
            out.append((lo+hi)/2)
        x=nx; prev=cv
    return out[s-1]

def field_square(m,n):
    x=np.linspace(0,1,G); X,Y=np.meshgrid(x,x)
    u=np.cos(n*PI*X)*np.cos(m*PI*Y)-np.cos(m*PI*X)*np.cos(n*PI*Y)
    return u,None
def field_disc(k,s):
    a=jzero(k,s)
    t=np.linspace(-1,1,G); X,Y=np.meshgrid(t,t)
    R=np.hypot(X,Y); TH=np.arctan2(Y,X)
    u=besselJ(k,a*np.clip(R,0,1))*np.cos(k*TH)
    return u, R>1.0
def field_sphere(l,m):
    """orthographic view of Y_l^m on the sphere"""
    t=np.linspace(-1,1,G); X,Y=np.meshgrid(t,t)
    R2=X*X+Y*Y; mask=R2>1.0
    Z=np.sqrt(np.clip(1-R2,0,None))
    th=np.arccos(np.clip(Z,-1,1)); ph=np.arctan2(Y,X)
    c=np.cos(th)
    pmm=np.ones_like(c)
    if m>0:
        ss=np.sqrt(np.maximum(0,(1-c)*(1+c))); f=1.0
        for i in range(1,m+1): pmm=pmm*(-f*ss); f+=2
    if l==m: P=pmm
    else:
        p1=c*(2*m+1)*pmm
        if l==m+1: P=p1
        else:
            for ll in range(m+2,l+1):
                pll=(c*(2*ll-1)*p1-(ll+m-1)*pmm)/(ll-m); pmm=p1; p1=pll
            P=p1
    u=P*np.cos(m*ph)
    lim=np.sqrt(np.clip(1-R2,0,None))          # limb shading
    return u*(0.25+0.75*lim), mask

def sand(u,mask,sigma=0.030):
    v=u/ (np.abs(u).max()+1e-12)
    d=np.exp(-(v/sigma)**2)                     # density peaks where u = 0
    d=d/d.max()
    if mask is not None: d=np.where(mask,np.nan,d)
    return d

def card(fn,u,mask,kicker,headline,sub,size=(1080,1080)):
    W,H=size; dpi=100
    fig=plt.figure(figsize=(W/dpi,H/dpi),dpi=dpi); fig.patch.set_facecolor(PLATE)
    ah=0.605 if W==H else 0.55
    ax=fig.add_axes([0.055,1-ah-0.035,0.89,ah]); ax.set_facecolor(PLATE)
    ax.imshow(sand(u,mask),cmap=cmap,origin="lower",interpolation="bilinear",vmin=0,vmax=1)
    ax.set_aspect("equal"); ax.axis("off")
    nl=headline.count("\n")+1
    ty=1-ah-0.070
    fig.text(0.055,ty,kicker,color=GOLD,fontsize=16 if W==H else 15,fontweight="bold",
             family="DejaVu Sans",va="top")
    fig.text(0.055,ty-0.048,headline,color=SAND,fontsize=37 if W==H else 31,fontweight="bold",
             family="DejaVu Serif",va="top",linespacing=1.16)
    fig.text(0.055,0.072,sub,color=DIM,fontsize=15.5 if W==H else 14,family="DejaVu Sans",
             va="bottom",linespacing=1.45)
    fig.text(0.945,0.032,"EXP13 · XII Bienal SBM · Natal-RN",color=GOLD,fontsize=12.5,
             family="DejaVu Sans",ha="right",va="bottom",alpha=.92)
    fig.savefig(fn,facecolor=PLATE); plt.close(fig); print("  ",fn)

CARDS=[
 ("01_sand",   field_square(2,3), "MISTÉRIO 1",
  "Por que a areia\nforma desenhos\nno som?",
  "Onde a placa vibra, o grão é arremessado. Onde ela fica parada,\no grão se acumula. O desenho é o conjunto nodal: a solução\nda equação diferencial igual a zero."),
 ("02_saturn", field_disc(6,3),   "MISTÉRIO 2",
  "O hexágono de\nSaturno é uma\nonda estacionária",
  "cos(6θ) — simetria de ordem seis, verificada em Lean 4.\nO mesmo número de onda que o jato polar mantém há 40 anos."),
 ("03_star",   field_sphere(10,4),"MISTÉRIO 3",
  "Uma estrela tocou\na 93 Hz. Esta é\na forma.",
  "SGR 1806−20, 2004. Modos torsionais da crosta de um magnetar,\nindexados por harmônicos esféricos: 93 Hz → ℓ = 10."),
 ("04_chladni",field_square(3,5), "MISTÉRIO 4",
  "Chladni, 1787.\nExplicado.",
  "Ele passou o arco na borda da placa e a areia desenhou sozinha.\nLevou mais de um século até alguém escrever a equação."),
]
for name,(u,mk),k,h,s in CARDS:
    card(f"{name}.png",u,mk,k,h,s)
    card(f"{name}_wide.png",u,mk,k,h,s,size=(1200,675))
