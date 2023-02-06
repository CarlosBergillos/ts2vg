from math import atan, sqrt

import numpy as np
import pytest
from pytest import approx

import ts2vg
from fixtures import empty_ts, flat_ts, sample_ts, sample_ts_2


def test_basic(sample_ts):
    out_got = ts2vg.HorizontalVG().build(sample_ts).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_basic_2(sample_ts_2):
    out_got = ts2vg.HorizontalVG().build(sample_ts_2).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 3),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (3, 4),
        (3, 5),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_left_to_right(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right").build(sample_ts).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (2, 3),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(sqrt(2.0))),
        (1, 2, approx(sqrt(5.0))),
        (2, 3, approx(sqrt(2.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_sq_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="sq_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(2.0)),
        (1, 2, approx(5.0)),
        (2, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_v_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="v_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(-2.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_v_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="abs_v_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_h_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="h_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(1.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_h_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="abs_h_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(1.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_slope(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="slope").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(-2.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_slope(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="abs_slope").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_angle(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="angle").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (1, 2, approx(atan(-2.0))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_angle(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="left_to_right", weighted="abs_angle").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (1, 2, approx(atan(2.0))),
        (2, 3, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom").build(sample_ts).edges

    out_truth = [
        (1, 0),
        (1, 2),
        (2, 3),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(sqrt(2.0))),
        (1, 2, approx(sqrt(5.0))),
        (2, 3, approx(sqrt(2.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_sq_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="sq_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(2.0)),
        (1, 2, approx(5.0)),
        (2, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_v_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="v_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(-1.0)),
        (1, 2, approx(-2.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_v_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="abs_v_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_h_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="h_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(-1.0)),
        (1, 2, approx(1.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_h_distance(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="abs_h_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(1.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_slope(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="slope").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(-2.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_slope(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="abs_slope").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_angle(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="angle").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(atan(1.0))),
        (1, 2, approx(atan(-2.0))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_angle(sample_ts):
    out_got = ts2vg.HorizontalVG(directed="top_to_bottom", weighted="abs_angle").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(atan(1.0))),
        (1, 2, approx(atan(2.0))),
        (2, 3, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_adjacency_matrix(sample_ts):
    out_got = ts2vg.HorizontalVG().build(sample_ts).adjacency_matrix(triangle="upper")

    out_truth = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]

    np.testing.assert_array_equal(out_got, out_truth)


def test_degrees(sample_ts):
    out_got = ts2vg.HorizontalVG().build(sample_ts).degrees

    out_truth = [1, 2, 2, 1]

    np.testing.assert_array_equal(out_got, out_truth)


def test_not_built():
    with pytest.raises(ts2vg.graph.base.NotBuiltError):
        ts2vg.HorizontalVG().edges


def test_empty_ts(empty_ts):
    out_got = ts2vg.HorizontalVG().build(empty_ts).edges

    out_truth = []

    assert out_got == out_truth


def test_flat_ts(flat_ts):
    out_got = ts2vg.HorizontalVG().build(flat_ts).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (2, 3),
    ]

    assert out_got == out_truth


def test_with_xs(sample_ts):
    xs = [0.0, 1.0, 2.0, 2.1]

    out_got = ts2vg.HorizontalVG().build(sample_ts, xs=xs).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_with_incompatible_xs(sample_ts):
    xs = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

    with pytest.raises(ValueError):
        ts2vg.HorizontalVG().build(sample_ts, xs=xs)


def test_with_non_monotonic_increasing_xs(sample_ts):
    xs = [0.0, 4.0, 2.0, 3.0]

    with pytest.raises(ValueError):
        ts2vg.HorizontalVG().build(sample_ts, xs=xs)


def test_with_non_monotonic_increasing_xs_2(sample_ts):
    xs = [0.0, 0.0, 2.0, 3.0]

    with pytest.raises(ValueError):
        ts2vg.HorizontalVG().build(sample_ts, xs=xs)
