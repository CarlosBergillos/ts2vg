import numpy as np
import pytest


@pytest.fixture
def empty_ts():
    return []


@pytest.fixture
def sample_ts():
    return [3.0, 4.0, 2.0, 1.0]


@pytest.fixture
def sample_ts_2():
    return [0.25, 0.15, 1.50, -0.10, -0.30, 0.0, 0.20, 1.20, 1.85, -0.35]


@pytest.fixture
def flat_ts():
    return [1.0, 1.0, 1.0, 1.0]


@pytest.fixture
def linear_ts_small():
    return [
        9999 + 0.0,
        9999 + 0.1,
        9999 + 0.2,
        9999 + 0.3,
        9999 + 0.4,
        9999 + 0.5,
        9999 + 0.6,
        9999 + 0.7,
        9999 + 0.8,
        9999 + 0.9,
        9999 + 1.0,
    ]


@pytest.fixture
def linear_ts_large():
    return 99999999 + np.arange(0, 1_000, 0.1, dtype="float64")


@pytest.fixture
def linear_ts_large_negative():
    return -99999999 - np.arange(0, 1_000, 0.1, dtype="float64")
