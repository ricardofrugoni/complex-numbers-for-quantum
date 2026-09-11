"""Invariantes matemáticos, eventos dos controles e preservação da câmera."""

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.interactive_geometry import (
    EXPLORERS, normalized_amplitudes, unit_powers,
)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


@pytest.mark.parametrize("p", [0, 0.01, 0.25, 0.5, 0.99, 1])
def test_normalization_and_phase_invariance(p):
    for pa, pb in [(0, 0), (np.pi, -np.pi/3), (17.2, -103.5)]:
        a, b = normalized_amplitudes(p, pa, pb)
        assert abs(a)**2 == pytest.approx(p, abs=1e-14)
        assert abs(a)**2 + abs(b)**2 == pytest.approx(1, abs=1e-14)


@pytest.mark.parametrize("p,pa,pb", [(-0.1, 0, 0), (1.1, 0, 0),
    (np.nan, 0, 0), (0.5, np.inf, 0), (0.5, 0, np.nan)])
def test_invalid_amplitudes(p, pa, pb):
    with pytest.raises(ValueError):
        normalized_amplitudes(p, pa, pb)


def test_quarter_turn_powers_and_unit_norm():
    np.testing.assert_allclose(unit_powers(np.pi/2, 4), [1, 1j, -1, -1j, 1], atol=1e-14)
    np.testing.assert_allclose(abs(unit_powers(-0.721, 24)), 1, atol=1e-14)
    np.testing.assert_array_equal(unit_powers(1.2, 0), [1])


@pytest.mark.parametrize("n", [-1, 1.5, True])
def test_invalid_power_exponent(n):
    with pytest.raises(ValueError):
        unit_powers(0, n)


def test_origin_has_no_argument_and_no_arc():
    lab = EXPLORERS["plano"]().set_values(a=0, b=0)
    assert lab.values["argument"] is None
    assert len(lab.artists["argument"].get_xdata()) == 0
    lab.set_values(a=3, b=4)
    assert lab.values["modulus"] == 5
    np.testing.assert_allclose(lab.artists["conjugate"].get_ydata(), [0, -4])


def test_sum_cancels_and_translates_second_vector():
    lab = EXPLORERS["soma"]().set_values(a=2, b=-1, c=-2, d=1)
    assert lab.values["result"] == 0
    np.testing.assert_array_equal(lab.artists["translated"].get_xdata(), [2, 0])
    np.testing.assert_array_equal(lab.artists["translated"].get_ydata(), [-1, 0])


def test_multiplication_rotates_and_zero_collapses_grid():
    lab = EXPLORERS["multiplicacao"]().set_values(a=1, b=1, scale=1, angle=90)
    assert lab.values["result"] == pytest.approx(-1+1j)
    lab.set_values(scale=0)
    assert lab.values["result"] == 0
    np.testing.assert_allclose(lab.artists["grid"].get_segments(), 0, atol=0)


def test_euler_projections_and_camera_survive_parameter_changes():
    lab = EXPLORERS["euler3d"]()
    lab.axes[0].view_init(elev=12, azim=123)
    lab.set_values(radius=2, phase=90, turns=1, position=0)
    assert lab.values["current"] == pytest.approx(2j)
    np.testing.assert_allclose(abs(lab.values["z"]), 2, atol=1e-14)
    assert lab.axes[0].azim == 123
    assert lab.axes[0].elev == 12
    lab.set_values(radius=0)
    np.testing.assert_array_equal(lab.values["z"], 0)
    lab.reset_view()
    assert lab.axes[0].azim == -58


def test_surface_level_matches_squared_distance():
    lab = EXPLORERS["modulo3d"]().set_values(a=2, b=-2)
    assert lab.values["height"] == pytest.approx(8)
    x, y = lab.artists["level"].get_data()
    np.testing.assert_allclose(x*x + y*y, 8, atol=1e-13)


@pytest.mark.parametrize("name", ["euler3d", "modulo3d"])
def test_mouse_drag_rotates_3d_camera_without_changing_data(name):
    lab = EXPLORERS[name]()
    lab.fig.canvas.draw()
    ax = lab.axes[0]
    initial_angles = (ax.elev, ax.azim, ax.roll)
    initial_value = lab.values["current"] if name == "euler3d" else lab.values["height"]
    x, y = ax.transAxes.transform((0.5, 0.5))
    events = [("button_press_event", x, y),
              ("motion_notify_event", x + 50, y + 25),
              ("button_release_event", x + 50, y + 25)]
    for event, px, py in events:
        lab.fig.canvas.callbacks.process(event, MouseEvent(event, lab.fig.canvas, px, py, button=1))
    assert (ax.elev, ax.azim, ax.roll) != initial_angles
    value = lab.values["current"] if name == "euler3d" else lab.values["height"]
    assert value == initial_value


def test_amplitude_bars_and_zero_phase():
    lab = EXPLORERS["amplitudes"]().set_values(p0=0, phase_alpha=120)
    assert lab.values["alpha"] == 0
    assert [b.get_height() for b in lab.artists["probabilities"]] == pytest.approx([0, 1])
    assert "indefinido" in lab.artists["readout"].get_text()
    assert lab.values["relative_phase"] is None
    assert lab.values["interference_probabilities"] == pytest.approx([0.5, 0.5])


def test_relative_phase_changes_second_basis_and_global_phase_preserves_both():
    lab = EXPLORERS["amplitudes"]().set_values(p0=0.5, phase_alpha=0, phase_beta=0)
    assert lab.values["interference_probabilities"] == pytest.approx([1, 0], abs=1e-14)
    lab.set_values(phase_beta=180)
    assert lab.values["probabilities"] == pytest.approx([0.5, 0.5])
    assert lab.values["interference_probabilities"] == pytest.approx([0, 1], abs=1e-14)
    assert [b.get_height() for b in lab.artists["interference_probabilities"]] == pytest.approx([0, 1])
    # Um deslocamento comum de +37° preserva as duas distribuições.
    lab.set_values(p0=0.75, phase_alpha=-40, phase_beta=65)
    before = lab.values.copy()
    lab.set_values(phase_alpha=-3, phase_beta=102)
    assert lab.values["alpha"] != pytest.approx(before["alpha"])
    for key in ("probabilities", "interference_probabilities", "relative_phase"):
        assert lab.values[key] == pytest.approx(before[key])


@pytest.mark.parametrize("p", [0, 0.2, 0.5, 0.9, 1])
def test_second_basis_agrees_with_interference_formula(p):
    lab = EXPLORERS["amplitudes"]().set_values(p0=p, phase_alpha=30, phase_beta=-90)
    expected_plus = 0.5 + np.sqrt(p*(1-p))*np.cos(np.radians(-120))
    assert lab.values["interference_probabilities"] == pytest.approx([expected_plus, 1-expected_plus])
    assert sum(lab.values["interference_probabilities"]) == pytest.approx(1)


def test_slider_mouse_events_change_math_and_reset_button_works():
    lab = EXPLORERS["plano"]()
    lab.fig.canvas.draw()
    slider = lab.sliders["a"]
    x, y = slider.ax.transData.transform((-2, 0.5))
    for event in ("button_press_event", "button_release_event"):
        lab.fig.canvas.callbacks.process(event, MouseEvent(event, lab.fig.canvas, x, y, button=1))
    assert lab.values["z"].real == pytest.approx(-2)
    button = lab.buttons["reset"]
    x, y = button.ax.transAxes.transform((0.5, 0.5))
    for event in ("button_press_event", "button_release_event"):
        lab.fig.canvas.callbacks.process(event, MouseEvent(event, lab.fig.canvas, x, y, button=1))
    assert lab.values["z"] == 3+2j


def test_programmatic_control_rejects_invalid_batch_without_partial_update():
    lab = EXPLORERS["potencias"]()
    with pytest.raises(ValueError):
        lab.set_values(angle=30, n=1.5)
    assert lab.sliders["angle"].val == 90
    with pytest.raises(ValueError):
        lab.set_values(angle=np.nan)
    with pytest.raises(KeyError):
        lab.set_values(missing=1)


@pytest.mark.parametrize("name", list(EXPLORERS))
def test_all_explorers_render_extremes_without_growing_artists(name, tmp_path):
    lab = EXPLORERS[name]()
    counts = [len(ax.get_children()) for ax in lab.axes]
    for edge in ("valmin", "valmax"):
        lab.set_values(**{key: getattr(slider, edge) for key, slider in lab.sliders.items()})
        lab.fig.canvas.draw()
        assert [len(ax.get_children()) for ax in lab.axes] == counts
    lab.reset()
    assert all(slider.val == slider.valinit for slider in lab.sliders.values())
    output = tmp_path / f"{name}.png"
    lab.fig.savefig(output, dpi=70)
    assert output.stat().st_size > 5000


@pytest.mark.parametrize("n", [2, 4, 7, 16])
def test_roots_are_distinct_unit_solutions_with_zero_sum(n):
    lab = EXPLORERS["raizes"]().set_values(n=n)
    roots = lab.values["roots"]
    assert len(roots) == n
    assert len(np.unique(np.round(roots, 12))) == n
    np.testing.assert_allclose(abs(roots), 1, atol=1e-13)
    np.testing.assert_allclose(roots**n, 1, atol=1e-13)
    assert abs(roots.sum()) < 1e-13
    if n == 4:
        np.testing.assert_allclose(roots, [1, 1j, -1, -1j], atol=1e-13)


def test_wave_quarter_turn_period_and_zero_amplitude():
    lab = EXPLORERS["ondas"]().set_values(amplitude=2, omega=2, phase=90, time=0)
    assert lab.values["current"] == pytest.approx(2j)
    assert lab.values["period"] == pytest.approx(np.pi)
    np.testing.assert_allclose(abs(lab.values["z"]), 2, atol=1e-13)
    lab.set_values(amplitude=0)
    np.testing.assert_array_equal(lab.values["z"], 0)
    assert "não é definida" in lab.artists["readout"].get_text()


def test_fourier_phase_changes_signal_but_not_amplitude_spectrum():
    lab = EXPLORERS["fourier"]().set_values(amplitude=1, harmonic=3, phase=0)
    before = lab.values["signal"].copy()
    np.testing.assert_allclose(lab.values["magnitudes"], [0, 1, 0, 1, 0, 0, 0, 0, 0], atol=1e-13)
    lab.set_values(phase=90)
    after = lab.values["signal"]
    assert not np.allclose(before, after)
    np.testing.assert_allclose(lab.values["magnitudes"], [0, 1, 0, 1, 0, 0, 0, 0, 0], atol=1e-13)
    assert lab.values["coefficients"][3] == pytest.approx(0.5j)
    reconstructed = np.fft.irfft(lab.values["coefficients"]*len(after), n=len(after))
    np.testing.assert_allclose(reconstructed, after, atol=1e-13)
    lab.set_values(amplitude=0)
    assert abs(lab.values["coefficients"][3]) < 1e-13
