"""Laboratórios geométricos com controles Matplotlib, sem alterar a API original.

No JupyterLab, execute %matplotlib widget antes de criar figuras.
Cada fábrica retorna um Explorer com figura, controles e valores calculados.
Ângulos da interface são dados em graus; cálculos usam radianos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.widgets import Button, Slider
import numpy as np

from .complex_geometry import conjugate, from_polar, scale_and_rotate

BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#008060"
GRAY = "#667085"
TAU = 2 * np.pi


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not np.isfinite(value):
        raise ValueError(f"{name} deve ser finito.")
    return value


def normalized_amplitudes(p0: float, phase_alpha: float, phase_beta: float):
    """Amplitudes normalizadas; fases em radianos e 0 <= p0 <= 1."""
    p0 = _finite(p0, "p0")
    if not 0 <= p0 <= 1:
        raise ValueError("p0 deve pertencer ao intervalo [0, 1].")
    pa = _finite(phase_alpha, "phase_alpha")
    pb = _finite(phase_beta, "phase_beta")
    return from_polar(np.sqrt(p0), pa), from_polar(np.sqrt(1 - p0), pb)


def unit_powers(theta: float, n: int):
    """Retorna z**k para k=0,...,n, com z=exp(i*theta)."""
    theta = _finite(theta, "theta")
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)) or n < 0:
        raise ValueError("n deve ser um inteiro não negativo.")
    return np.exp(1j * theta * np.arange(n + 1))


@dataclass
class Explorer:
    """Mantém controles vivos e permite inspecionar os resultados em Python.

Use set_values(a=..., b=...) para alterar os controles sem o mouse.
Os nomes e limites estão disponíveis no dicionário sliders.
"""

    fig: object
    axes: tuple
    sliders: dict = field(default_factory=dict)
    buttons: dict = field(default_factory=dict)
    artists: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)
    _update: Callable = field(default=lambda: None, repr=False)

    def set_values(self, **values):
        # Valida todas as entradas antes de modificar qualquer controle.
        for name, value in values.items():
            if name not in self.sliders:
                raise KeyError(f"Controle desconhecido: {name}")
            slider = self.sliders[name]
            value = _finite(value, name)
            if not slider.valmin <= value <= slider.valmax:
                raise ValueError(f"{name}: use [{slider.valmin}, {slider.valmax}].")
            if slider.valstep is not None:
                steps = (value - slider.valmin) / slider.valstep
                if not np.isclose(steps, round(steps), atol=1e-8, rtol=0):
                    raise ValueError(f"{name}: use incrementos de {slider.valstep}.")
        for name, value in values.items():
            self.sliders[name].set_val(float(value))
        return self

    def reset(self, _event=None):
        for slider in self.sliders.values():
            slider.reset()
        self.reset_view()

    def reset_view(self, _event=None):
        for ax in self.axes:
            if ax.name == "3d":
                ax.view_init(elev=26, azim=-58)
        self.fig.canvas.draw_idle()

    def close(self):
        plt.close(self.fig)


def _lab(title, subtitle, specs, *, three_d=False):
    fig = plt.figure(figsize=(12, 8.6), facecolor="white")
    fig.suptitle(title, fontsize=17, fontweight="bold", x=0.08, ha="left", y=0.975)
    fig.text(0.08, 0.925, subtitle, fontsize=10, color=GRAY)
    grid = fig.add_gridspec(1, 2, left=0.08, right=0.94, bottom=0.40,
                            top=0.85, wspace=0.36)
    left = fig.add_subplot(grid[0, 0], projection="3d" if three_d else None)
    right = fig.add_subplot(grid[0, 1])
    lab = Explorer(fig, (left, right))
    # Callbacks Matplotlib usam referências fracas; a figura possui o laboratório.
    fig._complex_geometry_explorer = lab
    for index, (name, label, low, high, initial, step) in enumerate(specs):
        area = fig.add_axes((0.25, 0.225 - 0.043 * index, 0.56, 0.022))
        lab.sliders[name] = Slider(area, label, low, high, valinit=initial,
                                   valstep=step, color=BLUE, valfmt="%g")
    lab.buttons["reset"] = Button(fig.add_axes((0.82, 0.055, 0.13, 0.04)), "Restaurar")
    lab.buttons["reset"].on_clicked(lab.reset)
    if three_d:
        lab.buttons["view"] = Button(fig.add_axes((0.65, 0.055, 0.15, 0.04)), "Restaurar vista")
        lab.buttons["view"].on_clicked(lab.reset_view)
        lab.reset_view()
    lab.artists["readout"] = fig.text(0.08, 0.29, "", fontsize=10, linespacing=1.7)
    return lab


def _connect(lab, update):
    lab._update = update

    def changed(_value):
        update()
        lab.fig.canvas.draw_idle()

    for slider in lab.sliders.values():
        slider.on_changed(changed)
    update()
    return lab


def _plane(ax, title, limit):
    ax.set(title=title, xlabel="Parte real", ylabel="Parte imaginária",
           xlim=(-limit, limit), ylim=(-limit, limit))
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color=GRAY, lw=0.7)
    ax.axvline(0, color=GRAY, lw=0.7)
    ax.grid(alpha=0.18)


def _line(ax, label, color=BLUE, style="-", marker="o"):
    return ax.plot([], [], linestyle=style, marker=marker, color=color,
                   label=label, lw=2, markersize=5)[0]


def _complex_line(line, points):
    z = np.asarray(points, dtype=complex)
    line.set_data(z.real, z.imag)


def _circle(ax, radius=1):
    t = np.linspace(0, TAU, 241)
    return ax.plot(radius * np.cos(t), radius * np.sin(t), "--", color=GRAY,
                   lw=0.9, label="Círculo de referência")[0]


def _fmt(z):
    return f"{z.real:.3f} {z.imag:+.3f}i"


def _phase(z):
    return "indefinido (z = 0)" if z == 0 else f"{np.degrees(np.angle(z)):.2f}°"


def complex_plane():
    """Plano, projeções, argumento, conjugado e comparação de módulos."""
    lab = _lab("Plano complexo e conjugação",
               "Mova a e b: observe o vetor, sua reflexão e a distância à origem.",
               [("a", "Parte real a", -4, 4, 3, 0.1),
                ("b", "Parte imaginária b", -4, 4, 2, 0.1)])
    ax, bars_ax = lab.axes
    _plane(ax, "Reflexão em relação ao eixo real", 6.1)
    zline = _line(ax, "z", BLUE)
    cline = _line(ax, "Conjugado z*", ORANGE, "--", "s")
    projection = _line(ax, "Projeções de z", GRAY, ":", "")
    circle = _circle(ax)
    arc = _line(ax, "Argumento principal", GREEN, "-", "")
    ax.legend(loc="upper left", fontsize=8)
    bars = bars_ax.bar(["|z|", "|z*|"], [0, 0], color=[BLUE, ORANGE])
    bars[1].set_hatch("//")
    labels = [bars_ax.text(i, 0, "", ha="center", va="bottom") for i in range(2)]
    bars_ax.set(title="A reflexão preserva o módulo", ylabel="Módulo", ylim=(0, 6.5))
    bars_ax.grid(axis="y", alpha=0.18)
    lab.artists.update(z=zline, conjugate=cline, argument=arc)

    def update():
        z = complex(lab.sliders["a"].val, lab.sliders["b"].val)
        r, phase = abs(z), np.angle(z)
        _complex_line(zline, [0, z])
        _complex_line(cline, [0, conjugate(z)])
        _complex_line(projection, [z.real, z, 1j * z.imag])
        t = np.linspace(0, TAU, 241)
        _complex_line(circle, r * np.exp(1j * t))
        _complex_line(arc, 0.8 * np.exp(1j * np.linspace(0, phase, 80)) if r else [])
        for bar, label in zip(bars, labels):
            bar.set_height(r)
            label.set_position((bar.get_x() + bar.get_width() / 2, r + 0.08))
            label.set_text(f"{r:.3f}")
        lab.artists["readout"].set_text(
            f"z = {_fmt(z)}     |z| = {r:.3f}     arg(z) = {_phase(z)}\n"
            f"z* = {_fmt(z.conjugate())}     z · z* = {r*r:.3f}")
        lab.values.update(z=z, modulus=r, argument=None if z == 0 else phase)

    return _connect(lab, update)


def addition():
    """Soma ponta a cauda, paralelogramo e desigualdade triangular."""
    lab = _lab("Soma como geometria de vetores",
               "Compare o caminho em duas etapas com o vetor que liga a origem ao resultado.",
               [("a", "Re(z₁)", -3, 3, 2, 0.1), ("b", "Im(z₁)", -3, 3, 1, 0.1),
                ("c", "Re(z₂)", -3, 3, -1, 0.1), ("d", "Im(z₂)", -3, 3, 2, 0.1)])
    ax, comp = lab.axes
    _plane(ax, "Soma ponta a cauda", 6.8)
    first = _line(ax, "z₁", BLUE)
    second = _line(ax, "z₂", ORANGE, "--", "s")
    shifted = _line(ax, "z₂ a partir de z₁", ORANGE, "-", "s")
    other = _line(ax, "z₁ a partir de z₂", GRAY, ":", "")
    result = _line(ax, "z₁ + z₂", GREEN, "-", "D")
    ax.legend(loc="upper left", fontsize=8)
    bars = comp.bar(["|z₁ + z₂|", "|z₁| + |z₂|"], [0, 0], color=[GREEN, GRAY])
    bars[1].set_hatch("//")
    comp.set(title="Comprimento direto ≤ caminho", ylabel="Comprimento", ylim=(0, 9.5))
    comp.grid(axis="y", alpha=0.18)
    lab.artists.update(result=result, translated=shifted)

    def update():
        a, b, c, d = (lab.sliders[k].val for k in ("a", "b", "c", "d"))
        z, w = complex(a, b), complex(c, d)
        _complex_line(first, [0, z])
        _complex_line(second, [0, w])
        _complex_line(shifted, [z, z + w])
        _complex_line(other, [w, z + w])
        _complex_line(result, [0, z + w])
        bars[0].set_height(abs(z + w))
        bars[1].set_height(abs(z) + abs(w))
        lab.artists["readout"].set_text(
            f"z₁ + z₂ = {_fmt(z + w)}\n"
            f"|z₁ + z₂| = {abs(z+w):.3f}    ≤    |z₁| + |z₂| = {abs(z)+abs(w):.3f}")
        lab.values.update(z=z, w=w, result=z + w)

    return _connect(lab, update)


def multiplication():
    """Transforma uma grade inteira por multiplicação complexa."""
    lab = _lab("Multiplicação: escala e rotação",
               "A mesma operação atua em cada ponto da grade. Os painéis usam a mesma escala.",
               [("a", "Re(z)", -2, 2, 1, 0.1), ("b", "Im(z)", -2, 2, 1, 0.1),
                ("scale", "Módulo de w", 0, 2, 1, 0.05),
                ("angle", "Ângulo de w (°)", -180, 180, 90, 1)])
    left, right = lab.axes
    for ax, title in zip(lab.axes, ["Antes: z", "Depois: w · z"]):
        _plane(ax, title, 6.1)
    base = np.array([[complex(k, -2), complex(k, 2)] for k in range(-2, 3)] +
                    [[complex(-2, k), complex(2, k)] for k in range(-2, 3)])

    def segments(points):
        return np.stack([points.real, points.imag], axis=-1)

    left.add_collection(LineCollection(segments(base), colors=GRAY, alpha=0.35))
    grid = LineCollection(segments(base), colors=ORANGE, alpha=0.45)
    right.add_collection(grid)
    source = _line(left, "z", BLUE)
    dest = _line(right, "w · z", ORANGE, "-", "D")
    left.legend(loc="upper left")
    right.legend(loc="upper left")
    lab.artists.update(result=dest, grid=grid)

    def update():
        z = complex(lab.sliders["a"].val, lab.sliders["b"].val)
        scale, angle = lab.sliders["scale"].val, np.radians(lab.sliders["angle"].val)
        w = from_polar(scale, angle)
        result = scale_and_rotate(z, scale, angle)
        _complex_line(source, [0, z])
        _complex_line(dest, [0, result])
        grid.set_segments(segments(base * w))
        lab.artists["readout"].set_text(
            f"w = {_fmt(w)}    w · z = {_fmt(result)}\n"
            f"|wz| = {abs(result):.3f}    arg(wz) = {_phase(result)}"
            + ("    Escala zero: a grade colapsa na origem." if scale == 0 else ""))
        lab.values.update(z=z, w=w, result=result)

    return _connect(lab, update)


def euler_helix():
    """Gráfico 3D (Re z, Im z, t) de z(t)=r exp(i(t+phi))."""
    lab = _lab("Euler em 3D: círculo, hélice e projeções",
               "Arraste o gráfico 3D para girar a câmera. O terceiro eixo é o parâmetro t, em radianos.",
               [("radius", "Módulo r", 0, 2, 1, 0.05),
                ("phase", "Fase inicial (°)", -180, 180, 0, 1),
                ("turns", "Voltas", 0.5, 4, 2, 0.5),
                ("position", "Posição no percurso", 0, 1, 0.25, 0.01)], three_d=True)
    ax, components = lab.axes
    ax.set(xlabel="Re(z)", ylabel="Im(z)", zlabel="t (rad)",
           xlim=(-2.3, 2.3), ylim=(-2.3, 2.3), title="(Re z(t), Im z(t), t)")
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_box_aspect((1, 1, 1.35))
    helix, = ax.plot([], [], [], color=BLUE, lw=2)
    circle, = ax.plot([], [], [], color=GRAY, ls="--", lw=1)
    radial, = ax.plot([], [], [], color=ORANGE, marker="o", lw=2)
    drop, = ax.plot([], [], [], color=GRAY, ls=":")
    re = _line(components, "Re(z) = r cos(t + φ)", BLUE, "-", "")
    im = _line(components, "Im(z) = r sen(t + φ)", ORANGE, "--", "")
    cursor = components.axvline(0, color=GREEN, lw=1)
    points = _line(components, "Valores selecionados", GREEN, "", "o")
    components.set(title="Projeções do mesmo percurso", xlabel="t (rad)",
                   ylabel="Componente", ylim=(-2.3, 2.3))
    components.grid(alpha=0.18)
    components.legend(loc="upper right", fontsize=8)
    lab.artists.update(helix=helix, cursor=radial)

    def update():
        radius = lab.sliders["radius"].val
        phase = np.radians(lab.sliders["phase"].val)
        end = TAU * lab.sliders["turns"].val
        t = np.linspace(0, end, 601)
        z = radius * np.exp(1j * (t + phase))
        selected = end * lab.sliders["position"].val
        current = from_polar(radius, selected + phase)
        helix.set_data_3d(z.real, z.imag, t)
        u = radius * np.exp(1j * np.linspace(0, TAU, 241))
        circle.set_data_3d(u.real, u.imag, np.zeros_like(u.real))
        radial.set_data_3d([0, current.real], [0, current.imag], [selected, selected])
        drop.set_data_3d([current.real]*2, [current.imag]*2, [0, selected])
        ax.set_zlim(0, end)
        components.set_xlim(0, end)
        re.set_data(t, z.real)
        im.set_data(t, z.imag)
        cursor.set_xdata([selected, selected])
        points.set_data([selected, selected], [current.real, current.imag])
        lab.artists["readout"].set_text(
            f"t = {selected:.3f} rad    z(t) = {_fmt(current)}    |z(t)| = {abs(current):.3f}\n"
            "A câmera muda a vista; r e φ mudam a curva. t não é uma terceira parte do número complexo.")
        lab.values.update(t=t, z=z, selected=selected, current=current)

    return _connect(lab, update)


def powers():
    """Potências inteiras de módulo 1 e argumento principal versus acumulado."""
    lab = _lab("Potências como rotações sucessivas",
               "Cada ponto é zᵏ. Os segmentos mostram a ordem dos passos discretos.",
               [("angle", "Ângulo de z (°)", -180, 180, 90, 1),
                ("n", "Expoente máximo n", 0, 24, 8, 1)])
    ax, phases = lab.axes
    _plane(ax, "Órbita no círculo unitário", 1.3)
    _circle(ax)
    orbit = _line(ax, "z⁰, z¹, …, zⁿ", BLUE, "--", "o")
    end = _line(ax, "Último ponto zⁿ", ORANGE, "", "D")
    ax.legend(loc="upper left", fontsize=8)
    accumulated = _line(phases, "Ângulo acumulado kθ", BLUE, "-", "o")
    principal = _line(phases, "Argumento principal", ORANGE, "", "s")
    phases.axhline(180, color=GRAY, ls=":", lw=1)
    phases.axhline(-180, color=GRAY, ls=":", lw=1)
    phases.set(title="Mesma direção, ângulos diferentes", xlabel="Expoente k", ylabel="Ângulo (°)")
    phases.grid(alpha=0.18)
    phases.legend(loc="upper left", fontsize=8)
    lab.artists.update(orbit=orbit, principal=principal)

    def update():
        angle, n = lab.sliders["angle"].val, int(lab.sliders["n"].val)
        z = unit_powers(np.radians(angle), n)
        k = np.arange(n + 1)
        _complex_line(orbit, z)
        _complex_line(end, [z[-1]])
        accumulated.set_data(k, k * angle)
        principal.set_data(k, np.degrees(np.angle(z)))
        phases.set_xlim(-0.5, max(1, n) + 0.5)
        phases.set_ylim(min(-210, n * angle - 30), max(210, n * angle + 30))
        lab.artists["readout"].set_text(
            f"z = exp(iθ)    zⁿ = {_fmt(z[-1])}    |zⁿ| = {abs(z[-1]):.3f}\n"
            f"nθ = {n*angle:.1f}°    arg(zⁿ) = {_phase(z[-1])}    Direções equivalentes módulo 360°.")
        lab.values.update(powers=z, accumulated=k * np.radians(angle))

    return _connect(lab, update)


def modulus_surface():
    """Superfície |a+bi|² e curvas de nível; altura não é uma coordenada complexa."""
    lab = _lab("Módulo ao quadrado: superfície e curvas de nível",
               "Arraste a superfície para girar. Compare a altura h com a distância no plano.",
               [("a", "Parte real a", -2, 2, 1, 0.1),
                ("b", "Parte imaginária b", -2, 2, 1, 0.1)], three_d=True)
    ax, plane = lab.axes
    grid = np.linspace(-2.9, 2.9, 65)
    x, y = np.meshgrid(grid, grid)
    height = x*x + y*y
    ax.plot_surface(x, y, height, cmap="cividis", alpha=0.65, linewidth=0,
                    rcount=45, ccount=45, vmin=0, vmax=17)
    ax.set(xlabel="Re(z) = a", ylabel="Im(z) = b", zlabel="h = |z|²",
           title="h = a² + b²", xlim=(-2.9, 2.9), ylim=(-2.9, 2.9), zlim=(0, 17))
    ax.set_box_aspect((1, 1, 1))
    stem, = ax.plot([], [], [], color=ORANGE, marker="o", lw=3)
    level3d, = ax.plot([], [], [], color=BLUE, lw=2)
    _plane(plane, "Curvas de nível de h", 3.1)
    contours = plane.contour(x, y, height, levels=[1, 2, 4, 6, 8, 12], colors=GRAY,
                             linewidths=0.7, alpha=0.65)
    plane.clabel(contours, inline=True, fontsize=8, fmt="%g")
    vector = _line(plane, "z", ORANGE, "-", "D")
    level = _line(plane, "Mesmo |z|²", BLUE, "-", "")
    plane.legend(loc="upper left", fontsize=8)
    lab.artists.update(stem=stem, level=level)

    def update():
        a, b = lab.sliders["a"].val, lab.sliders["b"].val
        z = complex(a, b)
        h = abs(z)**2
        u = abs(z) * np.exp(1j * np.linspace(0, TAU, 241))
        stem.set_data_3d([a, a], [b, b], [0, h])
        level3d.set_data_3d(u.real, u.imag, np.full(u.shape, h))
        _complex_line(vector, [0, z])
        _complex_line(level, u)
        lab.artists["readout"].set_text(
            f"z = {_fmt(z)}    |z| = {abs(z):.3f}    h = |z|² = {h:.3f}\n"
            "h é uma função do ponto. Um |z|² arbitrário não é automaticamente uma probabilidade.")
        lab.values.update(z=z, height=h)

    return _connect(lab, update)


def amplitudes():
    """Amplitudes normalizadas e comparação entre as bases 0/1 e +/−."""
    lab = _lab("Amplitudes complexas e probabilidades",
               "Mude a fase relativa: as barras 0/1 permanecem; as barras +/− podem mudar.",
               [("p0", "Probabilidade P(0)", 0, 1, 0.75, 0.01),
                ("phase_alpha", "Fase de α (°)", -180, 180, 45, 1),
                ("phase_beta", "Fase de β (°)", -180, 180, -60, 1)])
    ax, probs = lab.axes
    _plane(ax, "Dois coeficientes no plano complexo", 1.25)
    _circle(ax)
    alpha_line = _line(ax, "α", BLUE)
    beta_line = _line(ax, "β", ORANGE, "--", "s")
    ax.legend(loc="upper left", fontsize=8)
    bars = probs.bar([0, 1], [0.75, 0.25], color=[BLUE, ORANGE], width=0.65)
    bars[1].set_hatch("//")
    interference_bars = probs.bar([3, 4], [0, 0], color=[BLUE, ORANGE], width=0.65)
    interference_bars[1].set_hatch("//")
    labels = [probs.text(i, 0, "", ha="center", va="bottom", fontsize=9)
              for i in (0, 1, 3, 4)]
    probs.axvline(2, color=GRAY, ls=":", lw=1)
    probs.set(title="Duas escolhas de base de medição", ylabel="Probabilidade", ylim=(0, 1.22),
              xticks=[0, 1, 3, 4], xticklabels=["P(0)", "P(1)", "P(+)", "P(−)"])
    probs.text(0.5, 1.13, "Base 0/1", ha="center", color=GRAY, fontsize=9)
    probs.text(3.5, 1.13, "Base +/−", ha="center", color=GRAY, fontsize=9)
    probs.grid(axis="y", alpha=0.18)
    lab.artists.update(alpha=alpha_line, beta=beta_line, probabilities=bars,
                       interference_probabilities=interference_bars)

    def update():
        p0 = lab.sliders["p0"].val
        alpha, beta = normalized_amplitudes(p0, np.radians(lab.sliders["phase_alpha"].val),
                                            np.radians(lab.sliders["phase_beta"].val))
        _complex_line(alpha_line, [0, alpha])
        _complex_line(beta_line, [0, beta])
        probabilities = (abs(alpha)**2, abs(beta)**2)
        gamma_plus, gamma_minus = (alpha + beta)/np.sqrt(2), (alpha - beta)/np.sqrt(2)
        interference = (abs(gamma_plus)**2, abs(gamma_minus)**2)
        relative_phase = None if alpha == 0 or beta == 0 else np.angle(beta * alpha.conjugate())
        relative_text = ("indefinida (amplitude nula)" if relative_phase is None
                         else f"{np.degrees(relative_phase):.1f}°")
        for bar, label, p in zip((*bars, *interference_bars), labels, (*probabilities, *interference)):
            bar.set_height(p)
            label.set_position((bar.get_x() + bar.get_width()/2, p + 0.02))
            label.set_text(f"{p:.3f}")
        lab.artists["readout"].set_text(
            f"arg(α) = {_phase(alpha)}    arg(β) = {_phase(beta)}    Δφ = {relative_text}\n"
            "P(±) = |(α ± β)/√2|². Cada par soma 1; são escolhas distintas de medição.")
        lab.values.update(alpha=alpha, beta=beta, probabilities=probabilities,
                          interference_probabilities=interference, relative_phase=relative_phase)

    return _connect(lab, update)


def roots_of_unity():
    """As n raízes de z**n=1; vértices igualmente espaçados no círculo."""
    lab = _lab("Raízes da unidade: uma equação, muitas direções",
               "Mova n: cada vértice elevado a n retorna a 1. A soma dos vértices é zero.",
               [("n", "Número de raízes n", 2, 16, 5, 1)])
    ax, result_ax = lab.axes
    _plane(ax, "Um polígono no círculo unitário", 1.35)
    _circle(ax)
    polygon = _line(ax, "Raízes em ordem angular", BLUE, "-", "o")
    _plane(result_ax, "Todos os pontos wᵏ elevados a n", 1.35)
    _circle(result_ax)
    result = _line(result_ax, "Resultado: 1", ORANGE, "", "D")
    ax.legend(loc="lower left", fontsize=8)
    result_ax.legend(loc="lower left", fontsize=8)
    lab.artists.update(polygon=polygon, result=result)

    def update():
        n = int(lab.sliders["n"].val)
        roots = np.exp(1j * TAU * np.arange(n) / n)
        _complex_line(polygon, np.r_[roots, roots[0]])
        _complex_line(result, roots**n)
        lab.artists["readout"].set_text(
            f"wₖ = exp(2πik/{n})    k = 0, …, {n-1}    Separação angular: {360/n:.2f}°\n"
            f"Máximo |wₖⁿ − 1| = {np.max(abs(roots**n - 1)):.2e}    "
            f"|Σ wₖ| = {abs(roots.sum()):.2e}    Resíduos de ponto flutuante.")
        lab.values.update(n=n, roots=roots)

    return _connect(lab, update)


def waves():
    """Uma oscilação real como projeção de A exp(i(omega*t+phi))."""
    lab = _lab("Uma rotação vista de lado é uma oscilação",
               "A e φ mudam o fasor; ω controla sua velocidade angular. t é medido em segundos.",
               [("amplitude", "Amplitude A", 0, 2, 1, 0.05),
                ("omega", "ω (rad/s)", 0.5, 3, 1, 0.1),
                ("phase", "Fase φ (°)", -180, 180, 0, 1),
                ("time", "Instante t (s)", 0, 6, 1, 0.05)])
    ax, signal_ax = lab.axes
    _plane(ax, "z(t) e sua projeção real", 2.4)
    circle = _circle(ax)
    vector = _line(ax, "z(t)", BLUE)
    projection = _line(ax, "Re z(t)", ORANGE, "--", "s")
    signal = _line(signal_ax, "A cos(ωt + φ)", BLUE, "-", "")
    selected = _line(signal_ax, "Instante selecionado", ORANGE, "", "D")
    cursor = signal_ax.axvline(0, color=GRAY, ls=":")
    ax.legend(loc="lower left", fontsize=8)
    signal_ax.set(title="A parte real ao longo do tempo", xlabel="t (s)",
                  ylabel="Deslocamento (unidade arbitrária)", xlim=(0, 6), ylim=(-2.4, 2.4))
    signal_ax.legend(loc="lower left", fontsize=8)
    signal_ax.grid(alpha=0.18)

    def update():
        amplitude, omega, phase, time = (lab.sliders[k].val for k in
                                         ("amplitude", "omega", "phase", "time"))
        phi = np.radians(phase)
        t = np.linspace(0, 6, 601)
        z = amplitude * np.exp(1j * (omega*t + phi))
        current = amplitude * np.exp(1j * (omega*time + phi))
        _complex_line(circle, amplitude * np.exp(1j*np.linspace(0, TAU, 241)))
        _complex_line(vector, [0, current])
        _complex_line(projection, [current, current.real])
        signal.set_data(t, z.real)
        selected.set_data([time], [current.real])
        cursor.set_xdata([time, time])
        lab.artists["readout"].set_text(
            f"z(t) = A exp(i(ωt + φ))    z({time:.2f}) = {_fmt(current)}\n"
            f"Re z(t) = {current.real:.3f}    Período T = 2π/ω = {TAU/omega:.3f} s"
            + ("    A=0: sinal nulo; sua fase não é definida." if amplitude == 0 else ""))
        lab.values.update(t=t, z=z, current=current, period=TAU/omega)

    return _connect(lab, update)


def fourier_components():
    """Síntese de dois cossenos e espectro de amplitudes unilateral via DFT."""
    lab = _lab("Fourier: uma forma, duas frequências",
               "Mude a fase da segunda componente: a forma muda, mas seu espectro de amplitudes permanece.",
               [("amplitude", "Amplitude da 2ª componente", 0, 1.5, 0.5, 0.05),
                ("harmonic", "Harmônico k", 2, 8, 3, 1),
                ("phase", "Fase φ (°)", -180, 180, 0, 1)])
    ax, spectrum_ax = lab.axes
    first = _line(ax, "cos(t)", GRAY, "--", "")
    second = _line(ax, "A cos(kt + φ)", ORANGE, ":", "")
    total = _line(ax, "Soma", BLUE, "-", "")
    ax.set(title="Síntese no domínio do parâmetro t", xlabel="t (rad)",
           ylabel="Sinal", xlim=(0, TAU), ylim=(-2.8, 2.8))
    ax.grid(alpha=0.18)
    ax.legend(loc="lower left", fontsize=8)
    bars = spectrum_ax.bar(np.arange(9), np.zeros(9), color=BLUE)
    spectrum_ax.set(title="Amplitudes dos cossenos", xlabel="Harmônico",
                    ylabel="Amplitude (espectro unilateral)", ylim=(0, 1.7), xticks=range(9))
    spectrum_ax.grid(axis="y", alpha=0.18)
    lab.artists["spectrum"] = bars

    def update():
        amplitude = lab.sliders["amplitude"].val
        k = int(lab.sliders["harmonic"].val)
        phase = np.radians(lab.sliders["phase"].val)
        t = np.linspace(0, TAU, 512, endpoint=False)
        a, b = np.cos(t), amplitude*np.cos(k*t + phase)
        signal = a + b
        coefficients = np.fft.rfft(signal) / len(signal)
        magnitudes = 2*abs(coefficients[:9])
        magnitudes[0] /= 2  # DC não possui um parceiro de frequência negativa.
        first.set_data(t, a)
        second.set_data(t, b)
        total.set_data(t, signal)
        for bar, magnitude in zip(bars, magnitudes):
            bar.set_height(magnitude)
        lab.artists["readout"].set_text(
            f"s(t) = cos(t) + {amplitude:g} cos({k}t + φ)    φ = {np.degrees(phase):g}°\n"
            f"Coeficiente complexo c_{k} = {_fmt(coefficients[k])}    "
            f"|c_{k}| = {abs(coefficients[k]):.3f}    "
            "Cada cosseno não nulo divide sua amplitude entre ±k.")
        lab.values.update(t=t, signal=signal, coefficients=coefficients, magnitudes=magnitudes)

    return _connect(lab, update)


EXPLORERS = {
    "plano": complex_plane,
    "soma": addition,
    "multiplicacao": multiplication,
    "euler3d": euler_helix,
    "potencias": powers,
    "modulo3d": modulus_surface,
    "amplitudes": amplitudes,
    "raizes": roots_of_unity,
    "ondas": waves,
    "fourier": fourier_components,
}
