"""Prova as pausas exatas e a geometria da volta no círculo unitário."""
import numpy as np
from pathlib import Path
from PIL import Image, ImageSequence
from scripts.generate_book_assets import quarter_turn_frames


def test_one_second_at_each_quadrant_and_full_positive_turn():
    fps = 20
    frames = quarter_turn_frames(fps)
    assert frames[0] == 0 and frames[-1] == 2*np.pi
    assert np.all(np.diff(frames) >= 0)
    for k in (1, 2, 3, 4):
        selected = np.isclose(frames, k*np.pi/2, rtol=0, atol=1e-12)
        assert selected.sum() / fps == 1
        np.testing.assert_allclose(np.exp(1j*frames[selected]), (1j)**k, atol=1e-12)


def test_exported_gif_has_four_exact_one_second_pauses():
    path = Path(__file__).resolve().parents[1] / "assets/book/quatro_rotacoes.gif"
    with Image.open(path) as gif:
        pauses = [frame.info["duration"] for frame in ImageSequence.Iterator(gif)
                  if frame.info["duration"] >= 1000]
    assert pauses == [1000, 1000, 1000, 1000]
