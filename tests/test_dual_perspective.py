from math import atan, sqrt

import numpy as np
import pytest
from pytest import approx

import ts2vg
from fixtures import empty_ts, flat_ts, sample_ts


def test_dual_perspective_ttb():
    with pytest.raises(ValueError):
        ts2vg.NaturalVG(directed="top_to_bottom", dual_perspective=True)


def test_dual_perspective_only_degrees(sample_ts):
    vg = ts2vg.NaturalVG(dual_perspective=True)

    with pytest.raises(ValueError):
        vg.build(sample_ts, only_degrees=True)


def test_dual_perspective(sample_ts):
    out_got = ts2vg.NaturalVG(dual_perspective=True).build(sample_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_dual_perspective_ltr(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", dual_perspective=True).build(sample_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_distance(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="distance", dual_perspective=True).build(sample_ts).edges
    )

    out_truth = [
        (0, 1, approx(sqrt(2.0))),
        (0, 2, approx(sqrt(5.0))),
        (0, 3, approx(sqrt(13.0))),
        (1, 2, approx(sqrt(5.0))),
        (1, 3, approx(sqrt(13.0))),
        (2, 3, approx(sqrt(2.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_sq_distance(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="sq_distance", dual_perspective=True).build(sample_ts).edges
    )

    out_truth = [
        (0, 1, approx(2.0)),
        (0, 2, approx(5.0)),
        (0, 3, approx(13.0)),
        (1, 2, approx(5.0)),
        (1, 3, approx(13.0)),
        (2, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_h_distance(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="h_distance", dual_perspective=True).build(sample_ts).edges
    )

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(2.0)),
        (0, 3, approx(3.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_abs_h_distance(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="abs_h_distance", dual_perspective=True)
        .build(sample_ts)
        .edges
    )

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(2.0)),
        (0, 3, approx(3.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_v_distance(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="v_distance", dual_perspective=True).build(sample_ts).edges
    )

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(-1.0)),
        (0, 3, approx(-2.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-3.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_abs_v_distance(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="abs_v_distance", dual_perspective=True)
        .build(sample_ts)
        .edges
    )

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(1.0)),
        (0, 3, approx(2.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(3.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_slope(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="slope", dual_perspective=True).build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(-0.5)),
        (0, 3, approx(-2.0 / 3.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-1.5)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_abs_slope(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="abs_slope", dual_perspective=True).build(sample_ts).edges
    )

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(0.5)),
        (0, 3, approx(2.0 / 3.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(1.5)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_angle(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="angle", dual_perspective=True).build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (0, 2, approx(atan(-0.5))),
        (0, 3, approx(atan(-2.0 / 3.0))),
        (1, 2, approx(atan(-2.0))),
        (1, 3, approx(atan(-1.5))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_dual_perspective_ltr_abs_angle(sample_ts):
    out_got = (
        ts2vg.NaturalVG(directed="left_to_right", weighted="abs_angle", dual_perspective=True).build(sample_ts).edges
    )

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (0, 2, approx(atan(0.5))),
        (0, 3, approx(atan(2.0 / 3.0))),
        (1, 2, approx(atan(2.0))),
        (1, 3, approx(atan(1.5))),
        (2, 3, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_degrees(sample_ts):
    out_got = ts2vg.NaturalVG(dual_perspective=True).build(sample_ts).degrees

    out_truth = [3, 3, 3, 3]

    np.testing.assert_array_equal(out_got, out_truth)
