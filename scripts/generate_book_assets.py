"""Gera figuras vetoriais e uma animação matemática para o livro e o README.

Uso: python scripts/generate_book_assets.py [--skip-animation]
Não requer rede, LaTeX, ffmpeg ou bibliotecas além das dependências do projeto.
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "book"
NAVY, INK, MUTED = "#101c32", "#14263e", "#536478"
BLUE, TEAL, ORANGE = "#1467ae", "#087f8c", "#b34a16"
PAPER, GRID = "#f7f9fc", "#d8e2ee"
TAU = 2*np.pi


def save(fig, name):
    for extension in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{extension}", dpi=135, facecolor=fig.get_facecolor())
    plt.close(fig)


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
    fig = plt.figure(figsize=(13, 5.7), facecolor=NAVY)
    fig.text(0.055, 0.88, "UM NÚMERO. DUAS PERSPECTIVAS.", color="#75dfd0", size=12, weight="bold")
    fig.text(0.055, 0.69, "Coordenadas viram\nmagnitude e fase.", color="white", size=30, weight="bold", linespacing=1.25)
    fig.text(0.055, 0.43, r"$z = a+bi = r e^{i\theta}$", color="white", size=26)
    fig.text(0.055, 0.29, r"$e^{i\theta}=\cos\theta+i\sin\theta$", color="#75dfd0", size=21)
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
    ax.text(z.real+0.12, -0.3, r"$a=r\cos\theta$", color="#f7be6a", size=11)
    ax.text(-2.1, z.imag+0.12, r"$b=r\sin\theta$", color="#f7be6a", size=11)
    ax.text(-0.45, 0.95, r"$r=|z|$", color="white", size=13)
    save(fig, "hero")


def concept_cards():
    fig = plt.figure(figsize=(13, 2.7), facecolor=PAPER)
    entries = [(r"$a+bi$", "COORDENADAS", "um ponto no plano"),
               (r"$|z|$", "MAGNITUDE", "distância à origem"),
               (r"$\arg(z)$", "DIREÇÃO / FASE", "ângulo, se z ≠ 0"),
               (r"$z^*$", "CONJUGADO", "reflexão no eixo real"),
               (r"$e^{i\theta}$", "ROTAÇÃO", "um fator de módulo 1")]
    for i, (formula, title, caption) in enumerate(entries):
        x = 0.018+i*0.197
        box = FancyBboxPatch((x, .1), .18, .80, transform=fig.transFigure,
                             boxstyle="round,pad=0.009,rounding_size=0.025",
                             facecolor="white", edgecolor=GRID, lw=1)
        fig.add_artist(box)
        fig.text(x+.09, .63, formula, ha="center", color=BLUE, size=25)
        fig.text(x+.09, .38, title, ha="center", color=INK, size=10, weight="bold")
        fig.text(x+.09, .22, caption, ha="center", color=MUTED, size=9)
    save(fig, "conceitos")


def quarter_turns():
    fig, axes = plt.subplots(1, 5, figsize=(13, 3.7), facecolor=PAPER)
    fig.subplots_adjust(left=.035, right=.98, bottom=.20, top=.76, wspace=.45)
    fig.suptitle("Multiplicar por i: um quarto de volta, a cada passo", fontsize=19, color=INK, y=.94)
    for k, (ax, label) in enumerate(zip(axes, ["1", "i", "−1", "−i", "1"])):
        plane(ax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        t = np.linspace(0, TAU, 160)
        ax.plot(np.cos(t), np.sin(t), color=GRID)
        vector(ax, (1j)**k, BLUE if k < 4 else TEAL)
        ax.set_title(label, color=INK, fontsize=20, pad=10)
        ax.text(.5, -.15, f"{k} × 90°", transform=ax.transAxes, ha="center", color=MUTED, size=10)
        if k < 4:
            ax.text(1.14, .5, "× i →", transform=ax.transAxes, ha="center", color=TEAL, size=12)
    save(fig, "quatro_rotacoes")


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
    fig.text(.045, .17, "Uma amplitude não é um qubit completo: o estado puro exige um vetor normalizado (α, β).", size=12, color="white")
    fig.text(.045, .065, "Na base |0⟩, |1⟩: P(0) = |α|², P(1) = |β|² e |α|² + |β|² = 1. Se r = 0, a fase é indefinida.", size=10, color="#b9c9de")
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
        ax.plot(t, np.cos(t+phase), color=color, ls=style, label=f"φ = {np.degrees(phase):g}°")
    ax.set(title="Ondas · mesma amplitude, outra fase", xlabel="t (s), com ω = 1 rad/s", ylabel="Re z(t)")
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
    signal_ax.plot(t, np.cos(t), color=BLUE, label="cos θ · parte real")
    signal_ax.plot(t, np.sin(t), color=ORANGE, ls="--", label="sen θ · parte imaginária")
    cursor = signal_ax.axvline(0, color=TEAL)
    point_re, = signal_ax.plot([], [], "o", color=BLUE)
    point_im, = signal_ax.plot([], [], "s", color=ORANGE)
    signal_ax.set(xlim=(0, TAU), ylim=(-1.3, 1.3), xlabel="θ (rad)", ylabel="Componente")
    signal_ax.set_xticks([0, np.pi, TAU], ["0", "π", "2π"])
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
        readout.set_text(f"θ = {np.degrees(theta):05.1f}°     Re(z) = {z.real:+.2f}     Im(z) = {z.imag:+.2f}     |z| = 1")

    update(np.pi/3)
    fig.savefig(OUT / "euler_poster.png", dpi=135, facecolor=PAPER)
    if not skip_animation:
        movie = FuncAnimation(fig, update, frames=np.linspace(0, TAU, 60, endpoint=False),
                              interval=1000/12, cache_frame_data=False)
        movie.save(OUT / "euler.gif", writer=PillowWriter(fps=12), dpi=100)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-animation", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path",
                         "axes.titlecolor": INK, "axes.labelcolor": INK,
                         "text.color": INK, "svg.hashsalt": "complex-book"})
    for generator in [hero, concept_cards, quarter_turns, multiplication, quantum_bridge, roots, applications]:
        generator()
    rotation_animation(args.skip_animation)
    print(f"Figuras do livro: {OUT}")


if __name__ == "__main__":
    main()
