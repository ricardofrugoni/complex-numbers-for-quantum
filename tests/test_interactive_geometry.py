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
