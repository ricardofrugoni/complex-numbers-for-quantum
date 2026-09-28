"""Gera figuras vetoriais e uma animação matemática para o livro e o README.

Uso: python scripts/generate_book_assets.py [--skip-animation]
Não requer rede, LaTeX, ffmpeg ou bibliotecas além das dependências do projeto.
"""

import argparse
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch
from PIL import Image
import numpy as np
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.plot_style import register_montserrat
OUT = ROOT / "assets" / "book"
NAVY, INK, MUTED = "#080e19", "#e7edf8", "#a1adc3"
BLUE, TEAL, ORANGE = sns.color_palette(["#8fa8ff", "#7acddd", "#f093cd"]).as_hex()
PAPER, GRID = "#080e19", "#233149"
TAU = 2*np.pi


def save(fig, name):
    for extension in ("svg", "png"):
        path = OUT / f"{name}.{extension}"
        fig.savefig(path, dpi=135, facecolor=fig.get_facecolor())
        if extension == "svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n",
                            encoding="utf-8")
    plt.close(fig)


def save_gif(fig, update, values, name, *, fps, dpi=90):
    """Paleta única mantém o fundo estável e evita GIFs grandes por dithering."""
    fig.set_dpi(dpi)
    frames=[]
    palette=None
    for value in values:
        update(value)
        fig.canvas.draw()
        frame=Image.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("RGB")
        if palette is None:
            palette=frame.quantize(colors=128,dither=Image.Dither.NONE)
        frames.append(frame.quantize(palette=palette,dither=Image.Dither.NONE))
    frames[0].save(OUT/name,save_all=True,append_images=frames[1:],
                   duration=round(1000/fps),loop=0,optimize=False,disposal=1)


def plane(ax, limit=1.4, *, dark=False):
    fg = "#e7effa" if dark else INK
    grid = "#34465e" if dark else GRID
    ax.set_facecolor(NAVY if dark else PAPER)
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit), aspect="equal",
           xlabel="Parte real", ylabel="Parte imaginária")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color(grid)
    ax.tick_params(colors=fg, labelsize=9)
    ax.xaxis.label.set_color(fg)
    ax.yaxis.label.set_color(fg)
    ax.axhline(0, color=grid, lw=1)
    ax.axvline(0, color=grid, lw=1)
    ax.grid(color=grid, alpha=0.5, lw=0.5)


def vector(ax, z, color=BLUE, label=None):
    ax.annotate("", xy=(z.real, z.imag), xytext=(0, 0),
                arrowprops={"arrowstyle": "-|>", "lw": 2.6, "color": color})
    ax.scatter([z.real], [z.imag], s=42, color=color, zorder=4)
    if label:
        ax.annotate(label, (z.real, z.imag), xytext=(9, 10),
                    textcoords="offset points", fontsize=12, color=color)


def hero():
    fig = dark_canvas((13, 5.7))
    fig.text(0.055, 0.88, "UM NÚMERO. DUAS PERSPECTIVAS.", color="#75dfd0", size=12, weight="bold")
    fig.text(0.055, 0.69, "Coordenadas viram\nmagnitude e fase.", color="white", size=30, weight="bold", linespacing=1.25)
    fig.text(0.055, 0.43, r"$z = a+bi = r e^{i\theta}$", color="white", size=26)
    fig.text(0.055, 0.29, r"$r=|z|=\sqrt{a^2+b^2},\quad\theta=\arg(z)$", color="#75dfd0", size=20)
    fig.text(0.055, 0.12, "Explore o plano. Observe a rotação.\nDescubra onde essa geometria reaparece.", color="#b9c9de", size=12, linespacing=1.5)
    ax = fig.add_axes((0.58, 0.15, 0.36, 0.71))
    plane(ax, 2.3, dark=True)
    theta, radius = np.pi/3, 1.8
    z = radius*np.exp(1j*theta)
    t = np.linspace(0, TAU, 240)
    ax.plot(radius*np.cos(t), radius*np.sin(t), color="#617a9b", ls="--", lw=1.2)
    vector(ax, z, "#75dfd0", r"$z=re^{i\theta}$")
    ax.plot([z.real, z.real, 0], [0, z.imag, z.imag], ls=":", color="#f7be6a", lw=1.7)
    a = np.linspace(0, theta, 60)
    ax.plot(0.6*np.cos(a), 0.6*np.sin(a), color="#f7be6a", lw=2)
    ax.text(0.67, 0.28, r"$\theta$", color="#f7be6a", size=17)
    ax.text(z.real+0.12, -0.3, r"$a=\operatorname{Re}(z)$", color="#f7be6a", size=11)
    ax.text(-2.1, z.imag+0.12, r"$b=\operatorname{Im}(z)$", color="#f7be6a", size=11)
    ax.text(-0.45, 0.95, r"$r=|z|$", color="white", size=13)
    save(fig, "hero")


def concept_cards():
    fig = dark_canvas((13, 4.6))
    entries = [(r"$z=a+bi$", "COORDENADAS", r"$(a,b)\in\mathbb{R}^2$", .18, .66),
               (r"$r=|z|=\sqrt{a^2+b^2}$", "MAGNITUDE", r"$r\geq 0$", .50, .66),
               (r"$\theta=\arg(z)$", "ARGUMENTO", r"$z\neq 0$", .82, .66),
               (r"$\overline{z}=a-bi$", "CONJUGADO", r"$z\overline{z}=|z|^2$", .30, .24),
               (r"$e^{i\theta}=\cos\theta+i\sin\theta$", "ROTAÇÃO", r"$|e^{i\theta}|=1$", .72, .24)]
    for formula,title,caption,x,y in entries:
        fig.text(x,y+.19,title,ha="center",color=TEAL,size=10,weight="semibold")
        fig.text(x,y+.06,formula,ha="center",color=INK,size=23)
        fig.text(x,y-.07,caption,ha="center",color=MUTED,size=17)
    fig.add_artist(plt.Line2D([.07,.93],[.48,.48],transform=fig.transFigure,color=GRID,lw=1))
    save(fig, "conceitos")


def roadmap():
    stages=[("Fundamentos", "Uma linguagem para ir além dos reais.", r"$i^2=-1$"),
            ("Geometria", "Do par de coordenadas à distância.", r"$z=a+bi$"),
            ("Transformações", "Direção, reflexão e operações.", r"$z\mapsto\overline{z}$"),
            ("Magnitude e fase", "A mesma ideia em forma polar.", r"$z=re^{i\theta}$"),
            ("Rotações e simetrias", "Uma volta revela padrões.", r"$w_k=e^{2\pi i k/n}$"),
            ("A ponte quântica", "De ondas a amplitudes de um qubit.", r"$|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$")]
    for index,(title,subtitle,formula) in enumerate(stages):
        fig=plt.figure(figsize=(12,1.65),facecolor=NAVY)
        ax=fig.add_axes((0,0,1,1));ax.set(xlim=(0,12),ylim=(0,1.65));ax.set_axis_off()
        # Curvas alternadas mantêm a leitura de uma trilha entre as etapas.
        vertices=[(1.1,1.61),(10.6,1.61),(11.1,1.61),(11.1,1.16),(11.1,.48),(11.1,.04),(10.6,.04),(1.1,.04)]
        if index%2: vertices=[(12-x,y) for x,y in vertices]
        path=MplPath(vertices,[MplPath.MOVETO,MplPath.LINETO,MplPath.CURVE3,MplPath.CURVE3,MplPath.LINETO,MplPath.CURVE3,MplPath.CURVE3,MplPath.LINETO])
        ax.add_patch(PathPatch(path,fill=False,color="#797dde",lw=2.2))
        center=9.95 if index%2==0 else 2.05
        ax.add_patch(plt.Circle((center,.84),.49,fill=False,color="#9a94ed",lw=2))
        ax.text(center,.83,str(index+1),ha="center",va="center",color=INK,size=29,weight="semibold")
        x=1.65 if index%2==0 else 3.15
        ax.text(x,1.05,title,color=INK,size=17,weight="semibold")
        ax.text(x,.68,subtitle,color=MUTED,size=10)
        ax.text(x,.29,formula,color=TEAL,size=16)
        save(fig,f"roadmap_{index+1:02}")


def quarter_turn_frames(fps=20):
    """Uma volta positiva; cada quadrante termina em exatamente 1 s parado."""
    frames = [0.0]
    for k in range(4):
        start, end = k*np.pi/2, (k+1)*np.pi/2
        frames.extend(np.linspace(start, end, 2*fps+1)[1:-1])
        frames.extend([end]*fps)
    return np.asarray(frames)


def dark_canvas(figsize):
    fig = plt.figure(figsize=figsize, facecolor="#050911")
    backdrop = fig.add_axes((0,0,1,1), zorder=-2)
    backdrop.imshow(plt.imread(ROOT / "assets/backgrounds/night-sky.jpg"),
                    aspect="auto", extent=(0,1,0,1), alpha=.24)
    backdrop.set_axis_off()
    return fig


def quarter_turns(skip_animation=False):
    fig = dark_canvas((12,6.3))
    fig.text(.055,.91,"QUATRO PASSOS / UMA VOLTA",color="#7acddd",size=10,weight="semibold")
    fig.text(.055,.81,"Tudo volta\nao início.",color="#edf2ff",size=25,weight="semibold",va="top",linespacing=1.3)
    fig.text(.055,.55,r"$z=e^{i\theta}$",color="#f18bc2",size=29)
    angle_text = fig.text(.055,.39,"",color="#edf2ff",size=22)
    value_text = fig.text(.055,.30,"",color="#9ee9ef",size=18)
    fig.text(.055,.19,r"$|z|=1$",color="#a1adc3",size=16)
    fig.text(.055,.075,"ÂNGULOS POSITIVOS  /  SENTIDO ANTI-HORÁRIO",color="#a1adc3",size=8)
    ax = fig.add_axes((.40,.11,.57,.80),facecolor="none")
    ax.set(xlim=(-1.35,1.35),ylim=(-1.35,1.35),aspect="equal")
    ax.set_axis_off()
    t=np.linspace(0,TAU,400)
    ax.plot(np.cos(t),np.sin(t),color="#6387bd",lw=1.2,alpha=.7)
    ax.plot([-1.22,1.22],[0,0],color="#283650",lw=.8)
    ax.plot([0,0],[-1.22,1.22],color="#283650",lw=.8)
    for x,y,label in [(1.15,-.14,r"$0\,/\,2\pi$"),(-.10,1.18,r"$\pi/2$"),(-1.22,-.14,r"$\pi$"),(-.15,-1.28,r"$3\pi/2$")]:
        ax.text(x,y,label,color="#a9b9d4",size=14,ha="center")
    ax.text(1.22,.13,"Re",color="#7f90ad",size=10)
    ax.text(.13,1.20,"Im",color="#7f90ad",size=10)
    trail,=ax.plot([],[],color="#bb78cb",lw=2,alpha=.45)
    arrow=ax.annotate("",xy=(1,0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color="#f5a2d2",lw=2.4,mutation_scale=18))
    glow=ax.scatter([1],[0],s=260,color="#fa73c1",alpha=.12,zorder=4)
    point=ax.scatter([1],[0],s=32,color="#fff0fa",zorder=5)
    ax.scatter([0],[0],s=12,color="#7acddd")
    stops={1:(r"\pi/2","i"),2:(r"\pi","-1"),3:(r"3\pi/2","-i"),4:(r"2\pi","1")}

    def update(theta):
        z=np.exp(1j*theta)
        arrow.xy=(z.real,z.imag)
        point.set_offsets([[z.real,z.imag]]);glow.set_offsets([[z.real,z.imag]])
        trail_t=np.linspace(max(0,theta-.7),theta,70)
        trail.set_data(np.cos(trail_t),np.sin(trail_t))
        k=round(theta/(np.pi/2))
        if k in stops and np.isclose(theta,k*np.pi/2,atol=1e-10):
            label,value=stops[k]
            angle_text.set_text(rf"$\theta={label}\;\mathrm{{rad}}$")
            value_text.set_text(rf"$z={value}$")
        else:
            a,b=(0 if abs(v)<1e-10 else v for v in (z.real,z.imag))
            angle_text.set_text(rf"$\theta={theta:.2f}\;\mathrm{{rad}}$")
            value_text.set_text(rf"$z={a:.2f}{b:+.2f}i$")

    update(np.pi/2)
    fig.savefig(OUT/"quatro_rotacoes_poster.png",dpi=120,facecolor=fig.get_facecolor())
    if not skip_animation:
        save_gif(fig,update,quarter_turn_frames(),"quatro_rotacoes.gif",fps=20)
    plt.close(fig)


def multiplication():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7), facecolor=PAPER)
    fig.subplots_adjust(left=.08, right=.95, bottom=.17, top=.77, wspace=.55)
    fig.suptitle(r"$(1+i)\,i=-1+i$  ·  mesma distância, nova direção", fontsize=20, y=.95, color=INK)
    for ax, z, title, color in zip(axes, [1+1j, -1+1j], ["ANTES · z = 1 + i", "DEPOIS · iz = −1 + i"], [BLUE, ORANGE]):
        plane(ax, 1.9)
        ax.set_title(title, size=13, color=color, pad=12)
        t = np.linspace(0, TAU, 200)
        ax.plot(np.sqrt(2)*np.cos(t), np.sqrt(2)*np.sin(t), ls="--", color=GRID)
        vector(ax, z, color)
    fig.text(.5, .5, "+90°\n→", ha="center", color=TEAL, size=20)
    save(fig, "multiplicacao")


def quantum_bridge():
    fig = plt.figure(figsize=(13, 4), facecolor=NAVY)
    fig.text(.045, .84, "UMA AMPLITUDE COMPLEXA", size=12, color="#75dfd0", weight="bold")
    fig.text(.045, .49, r"$\alpha=r e^{i\varphi}$", size=32, color="white")
    fig.text(.34, .6, "MAGNITUDE", size=11, color="#b9c9de")
    fig.text(.34, .42, r"$r=|\alpha|$", size=23, color="white")
    fig.text(.56, .6, "FASE", size=11, color="#b9c9de")
    fig.text(.56, .42, r"$\varphi$", size=25, color="#75dfd0")
    fig.text(.73, .6, "MÓDULO AO QUADRADO", size=11, color="#b9c9de")
    fig.text(.73, .42, r"$|\alpha|^2=r^2$", size=24, color="#f7be6a")
    fig.text(.045, .17, r"Um qubit puro exige duas amplitudes normalizadas $(\alpha,\beta)$.", size=12, color="white")
    fig.text(.045, .065, r"$P(0)=|\alpha|^2,\quad P(1)=|\beta|^2,\quad |\alpha|^2+|\beta|^2=1$. Se $r=0$, a fase é indefinida.", size=10, color="#b9c9de")
    save(fig, "ponte_quantica")


def roots():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), facecolor=PAPER)
    fig.subplots_adjust(left=.06, right=.96, top=.74, bottom=.16, wspace=.36)
    fig.suptitle(r"$w_k=e^{2\pi i k/n}$  ·  raízes da unidade viram simetria", color=INK, size=21, y=.94)
    for ax, n in zip(axes, [3, 4, 5]):
        plane(ax)
        w = np.exp(1j*TAU*np.arange(n+1)/n)
        ax.plot(w.real, w.imag, "o-", color=BLUE, lw=2)
        t = np.linspace(0, TAU, 180)
        ax.plot(np.cos(t), np.sin(t), ls=":", color=MUTED, lw=.7)
        ax.set_title(f"n = {n} · passos de {360/n:g}°", color=INK, size=12, pad=10)
    save(fig, "raizes")


def applications():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=PAPER)
    fig.subplots_adjust(left=.07, right=.95, bottom=.19, top=.75, wspace=.36)
    fig.suptitle("Magnitude + fase: padrões que atravessam áreas", size=21, y=.94, color=INK)
    ax = axes[0]
    t = np.linspace(0, 4*np.pi, 600)
    for phase, color, style in [(0, BLUE, "-"), (np.pi/2, ORANGE, "--")]:
        ax.plot(t, np.cos(t+phase), color=color, ls=style, label=rf"$\varphi={phase:.2f}\;\mathrm{{rad}}$")
    ax.set(title="Ondas · mesma amplitude, outra fase", xlabel=r"$t$ (s), com $\omega=1$ rad/s", ylabel=r"$\operatorname{Re} z(t)$")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(color=GRID)
    ax = axes[1]
    plane(ax, 1.2)
    z = np.exp((-.12+1j)*t)
    ax.plot(z.real, z.imag, color=TEAL, lw=2)
    ax.plot([1], [0], "o", color=ORANGE)
    ax.set_title("Dinâmica · rotação com decaimento")
    save(fig, "aplicacoes")


def rotation_animation(skip_animation=False):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), facecolor=PAPER)
    fig.subplots_adjust(left=.075, right=.95, top=.77, bottom=.19, wspace=.4)
    fig.suptitle("Uma volta no plano. Duas projeções em movimento.", size=18, color=INK, y=.94)
    ax, signal_ax = axes
    plane(ax)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    t = np.linspace(0, TAU, 241)
    ax.plot(np.cos(t), np.sin(t), color=GRID, lw=1.4)
    radial, = ax.plot([], [], "o-", color=BLUE, lw=2.5)
    projection, = ax.plot([], [], ":", color=ORANGE, lw=1.7)
    arc, = ax.plot([], [], color=TEAL, lw=1.5)
    signal_ax.plot(t, np.cos(t), color=BLUE, label=r"$\cos\theta$ · parte real")
    signal_ax.plot(t, np.sin(t), color=ORANGE, ls="--", label=r"$\sin\theta$ · parte imaginária")
    cursor = signal_ax.axvline(0, color=TEAL)
    point_re, = signal_ax.plot([], [], "o", color=BLUE)
    point_im, = signal_ax.plot([], [], "s", color=ORANGE)
    signal_ax.set(xlim=(0, TAU), ylim=(-1.3, 1.3), xlabel=r"$\theta$ (rad)", ylabel="Componente")
    signal_ax.set_xticks([0, np.pi, TAU], [r"$0$", r"$\pi$", r"$2\pi$"])
    signal_ax.grid(color=GRID)
    signal_ax.legend(loc="lower center", fontsize=8)
    readout = fig.text(.5, .045, "", ha="center", fontsize=12, color=INK)

    def update(theta):
        z = np.exp(1j*theta)
        radial.set_data([0, z.real], [0, z.imag])
        projection.set_data([z.real, z.real, 0], [0, z.imag, z.imag])
        a = np.linspace(0, theta, 100)
        arc.set_data(.35*np.cos(a), .35*np.sin(a))
        cursor.set_xdata([theta, theta])
        point_re.set_data([theta], [z.real])
        point_im.set_data([theta], [z.imag])
        readout.set_text(rf"$\theta={theta:.2f}\;\mathrm{{rad}}\qquad \operatorname{{Re}}(z)={z.real:+.2f}\qquad \operatorname{{Im}}(z)={z.imag:+.2f}\qquad |z|=1$")

    update(np.pi/3)
    fig.savefig(OUT / "euler_poster.png", dpi=135, facecolor=PAPER)
    if not skip_animation:
        save_gif(fig,update,np.linspace(0,TAU,60,endpoint=False),"euler.gif",fps=12,dpi=100)
    plt.close(fig)


def laboratory_previews(skip_animation=False):
    fig = dark_canvas((12, 4.8))
    fig.text(.045,.91,"02 / ESCALA & ROTAÇÃO",size=10,color=TEAL,weight="semibold")
    fig.text(.045,.79,"Multiplicar é\ntransformar.",size=25,color=INK,weight="semibold",va="top",linespacing=1.25)
    fig.text(.045,.42,r"$z\mapsto \rho e^{i\theta}z$",size=23,color=BLUE)
    fig.text(.045,.26,"A mesma operação.\nUma nova geometria.",size=11,color=MUTED,linespacing=1.6)
    fig.text(.045,.075,"PRÉVIA ANIMADA / EXPLORE NO LABORATÓRIO",size=8,color=TEAL,weight="bold")
    status=fig.text(.67,.065,"",ha="center",size=12,color=INK)
    ax=fig.add_axes((.43,.20,.53,.67))
    plane(ax,3.4)
    ax.set_xlabel(r"$\operatorname{Re}(z)$")
    ax.set_ylabel(r"$\operatorname{Im}(z)$")
    base=[[complex(k,-2),complex(k,2)] for k in range(-2,3)]+[[complex(-2,k),complex(2,k)] for k in range(-2,3)]
    transformed=[]
    for points in base:
        p=np.array(points)
        ax.plot(p.real,p.imag,color=GRID,lw=1)
        transformed.append(ax.plot([],[],color=ORANGE,lw=1.3,alpha=.65)[0])
    ax.plot([0,1],[0,1],color=BLUE,lw=2,label=r"$z=1+i$")
    result,=ax.plot([],[],"o-",color=ORANGE,lw=2.8,label=r"$wz$")
    ax.legend(loc="upper right",fontsize=10,frameon=False)

    def update(theta):
        w=np.exp(1j*theta)
        for artist,points in zip(transformed,base):
            z=w*np.asarray(points);artist.set_data(z.real,z.imag)
        z=w*(1+1j)
        result.set_data([0,z.real],[0,z.imag])
        status.set_text(rf"$\theta={theta:.2f}\;\mathrm{{rad}}\qquad |wz|=\sqrt{{2}}$")
    update(np.pi/3)
    fig.savefig(OUT/"laboratorio_poster.png",dpi=120,facecolor=fig.get_facecolor())
    if not skip_animation:
        save_gif(fig,update,np.linspace(0,TAU,48,endpoint=False),"laboratorio.gif",fps=10)
    plt.close(fig)


def bloch_preview(skip_animation=False):
    fig=dark_canvas((12,6.3))
    fig.text(.055,.92,"ESFERA DE BLOCH",color="#7acddd",size=11,weight="semibold")
    fig.text(.945,.92,r"$|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$",ha="right",color=INK,size=18)
    ax=fig.add_axes((.17,.10,.66,.80),projection="3d",facecolor="none")
    u,v=np.meshgrid(np.linspace(0,TAU,49),np.linspace(0,np.pi,25))
    ax.plot_wireframe(np.sin(v)*np.cos(u),np.sin(v)*np.sin(u),np.cos(v),color="#6b92bb",alpha=.22,lw=.5,rstride=3,cstride=4)
    t=np.linspace(0,TAU,241)
    ax.plot(np.cos(t),np.sin(t),np.zeros_like(t),color="#7acddd",alpha=.5,lw=.9)
    i=np.arange(1200);z=1-2*(i+.5)/len(i);r=np.sqrt(1-z*z);a=i*np.pi*(3-np.sqrt(5))
    ax.scatter(r*np.cos(a),r*np.sin(a),z,s=.7,color="#acc8e8",alpha=.38,depthshade=False)
    ax.set(xlim=(-1.16,1.16),ylim=(-1.16,1.16),zlim=(-1.16,1.16))
    ax.set_axis_off();ax.set_box_aspect((1,1,1),zoom=1.55);ax.view_init(elev=20,azim=-60)
    ax.text(0,0,1.17,r"$|0\rangle$",ha="center",color=INK,fontsize=16)
    ax.text(0,0,-1.30,r"$|1\rangle$",ha="center",color=INK,fontsize=16)
    radial,=ax.plot([],[],[],"o-",color="#f5a2d2",lw=2.5,markersize=5)
    ax.plot(np.sqrt(.75)*np.cos(t),np.sqrt(.75)*np.sin(t),np.full_like(t,.5),color="#db88c0",lw=.9,alpha=.6)
    status=fig.text(.5,.075,"",ha="center",color=INK,size=16)

    def update(phi):
        x,y,z=np.sqrt(.75)*np.cos(phi),np.sqrt(.75)*np.sin(phi),.5
        radial.set_data_3d([0,x],[0,y],[0,z])
        status.set_text(rf"$\varphi={phi:.2f}\;\mathrm{{rad}}\qquad \|\mathbf{{r}}\|=1$")
    update(np.pi/3)
    fig.savefig(OUT/"bloch_poster.png",dpi=120,facecolor=fig.get_facecolor())
    if not skip_animation:
        save_gif(fig,update,np.linspace(0,TAU,64,endpoint=False),"bloch.gif",fps=10)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-animation", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", palette=[BLUE, ORANGE, TEAL],
                  rc={"axes.spines.top": False, "axes.spines.right": False,
                      "grid.color": GRID, "axes.edgecolor": GRID, "axes.facecolor": PAPER,
                      "xtick.color": MUTED, "ytick.color": MUTED, "mathtext.fontset": "stix"})
    plt.rcParams.update({"font.family": register_montserrat(), "svg.fonttype": "path",
                         "axes.titlecolor": INK, "axes.labelcolor": INK,
                         "text.color": INK, "svg.hashsalt": "complex-book"})
    for generator in [hero, concept_cards, roadmap, multiplication, quantum_bridge, roots, applications]:
        generator()
    rotation_animation(args.skip_animation)
    quarter_turns(args.skip_animation)
    laboratory_previews(args.skip_animation)
    bloch_preview(args.skip_animation)
    print(f"Figuras do livro: {OUT}")


if __name__ == "__main__":
    main()
