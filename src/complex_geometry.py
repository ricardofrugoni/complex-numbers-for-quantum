"""Funções auxiliares para estudar geometria de números complexos."""

from __future__ import annotations

import cmath
import math
from typing import Tuple

import matplotlib.pyplot as plt


def cartesian_parts(z: complex) -> tuple[float, float]:
    """Retorna (parte_real, parte_imaginaria)."""
    return float(z.real), float(z.imag)


def modulus(z: complex) -> float:
    """Retorna |z|."""
    return abs(z)


def argument(z: complex) -> float:
    """Retorna o argumento principal de z, em radianos."""
    return cmath.phase(z)


def conjugate(z: complex) -> complex:
    """Retorna o conjugado complexo de z."""
    return z.conjugate()


def to_polar(z: complex) -> Tuple[float, float]:
    """Retorna (r, theta), com theta em radianos."""
    return cmath.polar(z)


def from_polar(r: float, theta: float) -> complex:
    """Constrói r*exp(i*theta)."""
    if r < 0:
        raise ValueError("O módulo r deve ser não negativo.")
    return cmath.rect(r, theta)


def rotate(z: complex, theta: float) -> complex:
    """Rotaciona z por theta radianos sem alterar seu módulo."""
    return z * cmath.exp(1j * theta)


def scale_and_rotate(z: complex, scale: float, theta: float) -> complex:
    """Escala |z| por 'scale' e rotaciona por theta."""
    if scale < 0:
        raise ValueError("Use escala não negativa e represente inversão via ângulo.")
    return z * scale * cmath.exp(1j * theta)


def probability_from_amplitude(alpha: complex) -> float:
    """Calcula |alpha|^2."""
    return abs(alpha) ** 2


def plot_complex(
    z: complex,
    *,
    label: str = "z",
    ax=None,
    limits: tuple[float, float] | None = None,
):
    """Desenha z como vetor no plano complexo."""
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))

    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.arrow(
        0,
        0,
        z.real,
        z.imag,
        length_includes_head=True,
        head_width=max(0.06, 0.04 * max(1, abs(z))),
    )
    ax.scatter([z.real], [z.imag])
    ax.annotate(
        f"{label} = {z.real:.2f} {z.imag:+.2f}i",
        (z.real, z.imag),
        xytext=(8, 8),
        textcoords="offset points",
    )
    ax.set_xlabel("Parte real")
    ax.set_ylabel("Parte imaginária")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)

    if limits is None:
        lim = max(1.5, abs(z) * 1.3)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
    else:
        ax.set_xlim(*limits)
        ax.set_ylim(*limits)

    return ax
