import pytest
import math
from pysrc import intern


def test_pybind() -> None:
    assert intern.add(4, 5) == 9


def test_ftvf() -> None:
    vf = intern.FiveTickVolumeFeature()
    assert vf.compute_feature([[2, 1, False]]) == 1
    assert vf.compute_feature([[1, 1, False]]) == 2
    assert vf.compute_feature([[1, 1, False], [1, 1, True]]) == 4
    assert vf.compute_feature([[1, 1, False], [1, 1, True]]) == 6
    assert vf.compute_feature([[2, 1, False], [1, 1, True]]) == 8
    assert vf.compute_feature([[1, 1, False], [1, 1, True]]) == 9
    assert vf.compute_feature([[2, 1, False], [1, 1, True]]) == 10


def test_ntf() -> None:
    ntf = intern.NTradesFeature()
    assert ntf.compute_feature([[1, 1, False]]) == 1
    assert ntf.compute_feature([[2, 1, False], [2, 2, True]]) == 2


def test_ptf() -> None:
    ptf = intern.PercentBuyFeature()
    assert ptf.compute_feature([[1, 1, False]]) == 0
    assert ptf.compute_feature([[1, 1, False], [1, 1, True]]) == 0.5
    assert ptf.compute_feature([[1, 1, True]]) == 1


def test_psf() -> None:
    psf = intern.PercentSellFeature()
    assert psf.compute_feature([[1, 1, False]]), 1
    assert psf.compute_feature([[1, 1, False], [1, 1, True]]), 0.5
    assert math.isclose(
        psf.compute_feature([[1, 1, False], [1, 1, True], [1, 2, False]]),
        0.666666667,
        rel_tol=1e-6,
    )
