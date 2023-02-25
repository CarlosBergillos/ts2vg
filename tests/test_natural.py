from math import atan, sqrt

import numpy as np
import pytest
from pytest import approx

from fixtures import *
import ts2vg
from naive_implementations import natural_visibility_graph as naive_nvg


def test_basic(sample_ts):
    out_got = ts2vg.NaturalVG().build(sample_ts).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_basic_2(sample_ts_2):
    out_got = ts2vg.NaturalVG().build(sample_ts_2).edges

    out_truth = [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (3, 8),
        (4, 5),
        (4, 7),
        (4, 8),
        (5, 6),
        (5, 7),
        (5, 8),
        (6, 7),
        (7, 8),
        (8, 9),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_white_noise(white_noise_ts):
    ts = white_noise_ts
    xs = list(range(len(ts)))

    out_got = ts2vg.NaturalVG().build(ts, xs).edges

    out_truth = naive_nvg(ts, xs)

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_brownian_motion_ts(brownian_motion_ts):
    ts = brownian_motion_ts
    xs = list(range(len(ts)))

    out_got = ts2vg.NaturalVG().build(ts, xs).edges

    out_truth = naive_nvg(ts, xs)

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_left_to_right(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right").build(sample_ts).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(sqrt(2.0))),
        (1, 2, approx(sqrt(5.0))),
        (1, 3, approx(sqrt(13.0))),
        (2, 3, approx(sqrt(2.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_sq_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="sq_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(2.0)),
        (1, 2, approx(5.0)),
        (1, 3, approx(13.0)),
        (2, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_v_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="v_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-3.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_v_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_v_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(3.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_h_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="h_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_h_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_h_distance").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_slope(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="slope").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-1.5)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_slope(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_slope").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(1.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(1.5)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_angle(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="angle").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (1, 2, approx(atan(-2.0))),
        (1, 3, approx(atan(-1.5))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_left_to_right_abs_angle(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="abs_angle").build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
        (1, 2, approx(atan(2.0))),
        (1, 3, approx(atan(1.5))),
        (2, 3, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom").build(sample_ts).edges

    out_truth = [
        (1, 0),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(sqrt(2.0))),
        (1, 2, approx(sqrt(5.0))),
        (1, 3, approx(sqrt(13.0))),
        (2, 3, approx(sqrt(2.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_sq_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="sq_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(2.0)),
        (1, 2, approx(5.0)),
        (1, 3, approx(13.0)),
        (2, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_v_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="v_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(-1.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-3.0)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_v_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_v_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(3.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_h_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="h_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(-1.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_h_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_h_distance").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(1.0)),
        (1, 3, approx(2.0)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_slope(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="slope").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(-2.0)),
        (1, 3, approx(-1.5)),
        (2, 3, approx(-1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_slope(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_slope").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(1.0)),
        (1, 2, approx(2.0)),
        (1, 3, approx(1.5)),
        (2, 3, approx(1.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_angle(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="angle").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(atan(1.0))),
        (1, 2, approx(atan(-2.0))),
        (1, 3, approx(atan(-1.5))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_top_to_bottom_abs_angle(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom", weighted="abs_angle").build(sample_ts).edges

    out_truth = [
        (1, 0, approx(atan(1.0))),
        (1, 2, approx(atan(2.0))),
        (1, 3, approx(atan(1.5))),
        (2, 3, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_adjacency_matrix_upper(sample_ts):
    out_got = ts2vg.NaturalVG().build(sample_ts).adjacency_matrix(triangle="upper")

    out_truth = [
        [0, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]

    np.testing.assert_array_equal(out_got, out_truth)


def test_adjacency_matrix_lower(sample_ts):
    out_got = ts2vg.NaturalVG().build(sample_ts).adjacency_matrix(triangle="lower")

    out_truth = [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
    ]

    np.testing.assert_array_equal(out_got, out_truth)


def test_adjacency_matrix_both(sample_ts):
    out_got = ts2vg.NaturalVG().build(sample_ts).adjacency_matrix(triangle="both")

    out_truth = [
        [0, 1, 0, 0],
        [1, 0, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
    ]

    np.testing.assert_array_equal(out_got, out_truth)


def test_adjacency_matrix_directed_upper(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right").build(sample_ts)

    with pytest.raises(ValueError):
        vg.adjacency_matrix(triangle="upper")


def test_adjacency_matrix_directed_lower(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right").build(sample_ts)

    with pytest.raises(ValueError):
        vg.adjacency_matrix(triangle="lower")


def test_adjacency_matrix_directed_both(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right").build(sample_ts)
    out_got = vg.adjacency_matrix(triangle="both")

    out_truth = [
        [0, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]

    np.testing.assert_array_equal(out_got, out_truth)


def test_adjacency_matrix_directed_lower(sample_ts):
    vg = ts2vg.NaturalVG(directed="left_to_right")

    with pytest.raises(ts2vg.graph.base.NotBuiltError):
        vg.adjacency_matrix()


def test_degrees(sample_ts):
    out_got = ts2vg.NaturalVG().build(sample_ts).degrees

    out_truth = [1, 3, 2, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_degrees_in(sample_ts):
    out_got = ts2vg.NaturalVG().build(sample_ts).degrees_in

    out_truth = [0, 1, 1, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_degrees_out(sample_ts):
    out_got = ts2vg.NaturalVG().build(sample_ts).degrees_out

    out_truth = [1, 2, 1, 0]

    np.testing.assert_array_equal(out_got, out_truth)


def test_degrees_in_ltr(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right").build(sample_ts).degrees_in

    out_truth = [0, 1, 1, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_degrees_out_ltr(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right").build(sample_ts).degrees_out

    out_truth = [1, 2, 1, 0]

    np.testing.assert_array_equal(out_got, out_truth)


def test_degrees_in_ttb(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom").build(sample_ts).degrees_in

    out_truth = [1, 0, 1, 2]

    np.testing.assert_array_equal(out_got, out_truth)


def test_degrees_out_ttb(sample_ts):
    out_got = ts2vg.NaturalVG(directed="top_to_bottom").build(sample_ts).degrees_out

    out_truth = [0, 3, 1, 0]

    np.testing.assert_array_equal(out_got, out_truth)


def test_not_built():
    with pytest.raises(ts2vg.graph.base.NotBuiltError):
        ts2vg.NaturalVG().edges


def test_empty_ts(empty_ts):
    out_got = ts2vg.NaturalVG().build(empty_ts).edges

    out_truth = []

    assert out_got == out_truth


def test_flat_ts(flat_ts):
    out_got = ts2vg.NaturalVG().build(flat_ts).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (2, 3),
    ]

    assert out_got == out_truth


def test_with_xs(sample_ts):
    xs = [0.0, 1.0, 2.0, 2.1]

    out_got = ts2vg.NaturalVG().build(sample_ts, xs=xs).edges

    out_truth = [
        (0, 1),
        (1, 2),
        (2, 3),
    ]

    assert sorted(sorted(e) for e in out_got) == sorted(sorted(e) for e in out_truth)


def test_with_incompatible_xs(sample_ts):
    xs = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

    with pytest.raises(ValueError):
        ts2vg.NaturalVG().build(sample_ts, xs=xs)


def test_with_non_monotonic_increasing_xs(sample_ts):
    xs = [0.0, 4.0, 2.0, 3.0]

    with pytest.raises(ValueError):
        ts2vg.NaturalVG().build(sample_ts, xs=xs)


def test_with_non_monotonic_increasing_xs_2(sample_ts):
    xs = [0.0, 0.0, 2.0, 3.0]

    with pytest.raises(ValueError):
        ts2vg.NaturalVG().build(sample_ts, xs=xs)


def test_floating_point_linear(linear_ts_small):
    out_got = ts2vg.NaturalVG().build(linear_ts_small).edges

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
    out_got = ts2vg.NaturalVG().build(linear_ts_large).n_edges

    out_truth = len(linear_ts_large) - 1

    assert out_got == out_truth


def test_floating_point_linear_large_negative(linear_ts_large_negative):
    out_got = ts2vg.NaturalVG().build(linear_ts_large_negative).n_edges

    out_truth = len(linear_ts_large_negative) - 1

    assert out_got == out_truth
