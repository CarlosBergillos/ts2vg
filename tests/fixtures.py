import pytest


@pytest.fixture
def empty_ts():
    return []


@pytest.fixture
def sample_ts():
    return [3.0, 4.0, 2.0, 1.0]


@pytest.fixture
def flat_ts():
    return [1.0, 1.0, 1.0, 1.0]
