from math import atan, sqrt

import numpy as np
import pytest
from pytest import approx

import ts2vg
from fixtures import empty_ts, flat_ts, sample_ts


def test_unweighted_parametric(sample_ts):
    with pytest.raises(ValueError):
        ts2vg.NaturalVG(min_weight=0, max_weight=0).build(sample_ts)


def test_min_angle(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="angle", min_weight=0).build(sample_ts).edges

    out_truth = [
        (0, 1, approx(atan(1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_max_angle(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="angle", max_weight=0).build(sample_ts).edges

    out_truth = [
        (1, 2, approx(atan(-2.0))),
        (1, 3, approx(atan(-1.5))),
        (2, 3, approx(atan(-1.0))),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_min_h_distance(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="h_distance", min_weight=1.5).build(sample_ts).edges

    out_truth = [
        (1, 3, approx(2.0)),
    ]

    assert sorted(out_got) == sorted(out_truth)


def test_min_h_distance_2(sample_ts):
    out_got = ts2vg.NaturalVG(directed="left_to_right", weighted="h_distance", min_weight=2).build(sample_ts).edges

    out_truth = []

    assert sorted(out_got) == sorted(out_truth)
