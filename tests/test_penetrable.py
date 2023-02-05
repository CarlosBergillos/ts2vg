from math import atan, sqrt

import numpy as np
import pytest
from pytest import approx

import ts2vg
from fixtures import empty_ts, flat_ts, sample_ts, linear_ts_small, linear_ts_large, linear_ts_large_negative


def test_penetrable_0(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=0)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_penetrable_1(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_penetrable_2(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=2)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_penetrable_3(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=3)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_penetrable_1_ltr(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(sqrt(2.0))),
        (0, 2, approx(sqrt(5.0))),
        (1, 2, approx(sqrt(5.0))),
        (1, 3, approx(sqrt(13.0))),
        (2, 3, approx(sqrt(2.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_sq_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="sq_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(2.0)),
        (0, 2, approx(5.0)),
        (1, 2, approx(5.0)),
        (1, 3, approx(13.0)),
        (2, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_v_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="v_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(-1.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-3.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_abs_v_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_v_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(1.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(3.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_h_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="h_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(2.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_abs_h_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_h_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(2.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_slope(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="slope", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(-0.5)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-1.5)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_abs_slope(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_slope", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (0, 2, approx(0.5)),
        (1, 2, approx(2.0)),
        (1, 3, approx(1.5)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_angle(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="angle", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (0, 2, approx(atan(-0.5))),
        (1, 2, approx(atan(-2.0))),
        (1, 3, approx(atan(-1.5))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ltr_abs_angle(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_angle", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (0, 2, approx(atan(0.5))),
        (1, 2, approx(atan(2.0))),
        (1, 3, approx(atan(1.5))),
        (2, 3, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2),
        (1, 0),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(sqrt(5.0))),
        (1, 0, approx(sqrt(2.0))),
        (1, 2, approx(sqrt(5.0))),
        (1, 3, approx(sqrt(13.0))),
        (2, 3, approx(sqrt(2.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_sq_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="sq_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(5.0)),
        (1, 0, approx(2.0)),
        (1, 2, approx(5.0)),
        (1, 3, approx(13.0)),
        (2, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_v_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="v_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(-1.0)),
        (1, 0, approx(-1.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-3.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_abs_v_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_v_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(1.0)),
        (1, 0, approx(1.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(3.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_h_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="h_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(2.0)),
        (1, 0, approx(-1.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_abs_h_distance(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_h_distance", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(2.0)),
        (1, 0, approx(1.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_slope(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="slope", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(-0.5)),
        (1, 0, approx(1.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-1.5)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_abs_slope(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_slope", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(0.5)),
        (1, 0, approx(1.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(1.5)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_angle(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="angle", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(atan(-0.5))),
        (1, 0, approx(atan(1.0))),
        (1, 2, approx(atan(-2.0))),
        (1, 3, approx(atan(-1.5))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_ttb_abs_angle(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_angle", penetrable_limit=1)
    out_got = vg.build(sample_ts).edges

    out_truth = [
        (0, 2, approx(atan(0.5))),
        (1, 0, approx(atan(1.0))),
        (1, 2, approx(atan(2.0))),
        (1, 3, approx(atan(1.5))),
        (2, 3, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_penetrable_1_adjacency_matrix_upper(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(sample_ts).adjacency_matrix(triangle="upper")

    out_truth = [
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_degrees(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(sample_ts).degrees

    out_truth = [2, 3, 3, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_degrees_in(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(sample_ts).degrees_in

    out_truth = [0, 1, 2, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_degrees_out(sample_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(sample_ts).degrees_out

    out_truth = [2, 2, 1, 0]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_degrees_in_ltr(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", penetrable_limit=1)
    out_got = vg.build(sample_ts).degrees_in

    out_truth = [0, 1, 2, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_degrees_out_ltr(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right", penetrable_limit=1)
    out_got = vg.build(sample_ts).degrees_out

    out_truth = [2, 2, 1, 0]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_degrees_in_ttb(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", penetrable_limit=1)
    out_got = vg.build(sample_ts).degrees_in

    out_truth = [1, 0, 2, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_degrees_out_ttb(sample_ts):
    vg = ts2vg.NaturalVG(directed="top_to_bottom", penetrable_limit=1)
    out_got = vg.build(sample_ts).degrees_out

    out_truth = [1, 3, 1, 0]

    np.testing.assert_array_equal(out_got, out_truth)


def test_penetrable_1_empty(empty_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(empty_ts).edges

    out_truth = []

    assert out_got == out_truth


def test_penetrable_1_flat_ts(flat_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(flat_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert out_got == out_truth


def test_penetrable_1_flat_ts(flat_ts):
    vg = ts2vg.NaturalVG(penetrable_limit=2)
    out_got = vg.build(flat_ts).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert out_got == out_truth


def test_penetrable_1_with_xs(sample_ts):
    xs = [0.0, 1.0, 2.0, 2.1]

    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(sample_ts, xs=xs).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_penetrable_1_with_incompatible_xs(sample_ts):
    xs = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

    vg = ts2vg.NaturalVG(penetrable_limit=1)

    with pytest.raises(ValueError):
        vg.build(sample_ts, xs=xs)


def test_penetrable_1_with_non_monotonic_increasing_xs(sample_ts):
    xs = [0.0, 4.0, 2.0, 3.0]

    vg = ts2vg.NaturalVG(penetrable_limit=1)

    with pytest.raises(ValueError):
        vg.build(sample_ts, xs=xs)


def test_penetrable_1_with_non_monotonic_increasing_xs_2(sample_ts):
    xs = [0.0, 0.0, 2.0, 3.0]

    vg = ts2vg.NaturalVG(penetrable_limit=1)

    with pytest.raises(ValueError):
        vg.build(sample_ts, xs=xs)


def test_penetrable_1_floating_point_linear(linear_ts_small):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(linear_ts_small).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (3, 4),
        (3, 5),
        (4, 5),
        (4, 6),
        (5, 6),
        (5, 7),
        (6, 7),
        (6, 8),
        (7, 8),
        (7, 9),
        (8, 9),
        (8, 10),
        (9, 10),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_penetrable_2_floating_point_linear(linear_ts_small):
    vg = ts2vg.NaturalVG(penetrable_limit=2)
    out_got = vg.build(linear_ts_small).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 5),
        (4, 6),
        (4, 7),
        (5, 6),
        (5, 7),
        (5, 8),
        (6, 7),
        (6, 8),
        (6, 9),
        (7, 8),
        (7, 9),
        (7, 10),
        (8, 9),
        (8, 10),
        (9, 10),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_penetrable_1_floating_point_linear_large(linear_ts_large):
    vg = ts2vg.NaturalVG(penetrable_limit=1)
    out_got = vg.build(linear_ts_large).n_edges

    out_truth = 2 * len(linear_ts_large) - 3

    assert out_got == out_truth


def test_penetrable_100_floating_point_linear_large(linear_ts_large):
    n = len(linear_ts_large)
    m = 100

    vg = ts2vg.NaturalVG(penetrable_limit=m)
    out_got = vg.build(linear_ts_large).n_edges

    # number of edges of a linear time series of length n, with penetrable limit = m, is:
    #   |E| = n-1 + n-2 + ... + n-(m+1)
    #       = (m+1)*n - (1 + 2 + ... + m+1)

    out_truth = (m + 1) * n - ((m + 1) * (m + 2) / 2)

    assert out_got == out_truth


def test_penetrable_100_floating_point_linear_large_negative(linear_ts_large_negative):
    n = len(linear_ts_large_negative)
    m = 100

    vg = ts2vg.NaturalVG(penetrable_limit=m)
    out_got = vg.build(linear_ts_large_negative).n_edges

    out_truth = (m + 1) * n - ((m + 1) * (m + 2) / 2)

    assert out_got == out_truth
