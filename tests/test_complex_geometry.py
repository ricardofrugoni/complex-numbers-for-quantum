import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.complex_geometry import (
    conjugate,
    from_polar,
    modulus,
    probability_from_amplitude,
    rotate,
    to_polar,
)


def test_modulus_3_4_5():
    assert math.isclose(modulus(3 + 4j), 5.0)


def test_conjugate():
    assert conjugate(3 + 4j) == 3 - 4j


def test_polar_round_trip():
    z = 1 + 1j
    r, theta = to_polar(z)
    z2 = from_polar(r, theta)
    assert math.isclose(z.real, z2.real, abs_tol=1e-12)
    assert math.isclose(z.imag, z2.imag, abs_tol=1e-12)


def test_rotation_90_degrees():
    result = rotate(1 + 0j, math.pi / 2)
    assert math.isclose(result.real, 0.0, abs_tol=1e-12)
    assert math.isclose(result.imag, 1.0, abs_tol=1e-12)


def test_probability_from_amplitude():
    alpha = math.sqrt(0.75)
    assert math.isclose(probability_from_amplitude(alpha), 0.75)
