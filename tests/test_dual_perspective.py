from math import atan, sqrt

import numpy as np
import pytest
from pytest import approx

import ts2vg
from fixtures import empty_ts, flat_ts, sample_ts, linear_ts_small, linear_ts_large, linear_ts_large_negative


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


# TODO: test dual perspective with min_weight and max_weight
# TODO: test horizontal dual perspective?


def test_degrees(sample_ts):
    out_got = ts2vg.NaturalVG(dual_perspective=True).build(sample_ts).degrees

    out_truth = [3, 3, 3, 3]

    np.testing.assert_array_equal(out_got, out_truth)


# TODO: add more degree tests


def test_floating_point_linear(linear_ts_small):
    out_got = ts2vg.NaturalVG(dual_perspective=True).build(linear_ts_small).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_floating_point_linear_large(linear_ts_large):
    out_got = ts2vg.NaturalVG(dual_perspective=True).build(linear_ts_large).n_edges

    out_truth = len(linear_ts_large) - 1

    assert out_got == out_truth


def test_floating_point_linear_large_negative(linear_ts_large_negative):
    out_got = ts2vg.NaturalVG(dual_perspective=True).build(linear_ts_large_negative).n_edges

    out_truth = len(linear_ts_large_negative) - 1

    assert out_got == out_truth
