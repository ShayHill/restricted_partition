"""Test partitions.py

:author: Shay Hill
:created: 2023-03-03
"""

import pytest
from _pytest.fixtures import SubRequest

import restricted_partition as rp


@pytest.fixture(params=list(range(1, 17)))
def n(request: SubRequest) -> int:
    return request.param


@pytest.fixture(params=list(range(1, 17)))
def max_len(request: SubRequest) -> int:
    return request.param


class TestAccelAsc:
    def test_negative(self):
        """Follows convention that p(-1) == 0"""
        assert tuple(rp.iter_partition(-1)) == ()

    def test_0(self):
        """Follows convention that p(0) == 1"""
        assert tuple(rp.iter_partition(0)) == ([0],)

    def test_1(self):
        assert tuple(rp.iter_partition(1)) == ([1],)

    def test_2(self):
        assert tuple(rp.iter_partition(2)) == ([1, 1], [2])

    def test_7(self):
        assert tuple(rp.iter_partition(7)) == (
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 2],
            [1, 1, 1, 1, 3],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 4],
            [1, 1, 2, 3],
            [1, 1, 5],
            [1, 2, 2, 2],
            [1, 2, 4],
            [1, 3, 3],
            [1, 6],
            [2, 2, 3],
            [2, 5],
            [3, 4],
            [7],
        )

    def test_5(self):
        assert tuple(rp.iter_partition(5)) == (
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 3],
            [1, 2, 2],
            [1, 4],
            [2, 3],
            [5],
        )

    def test_max_len_is_n(self, n: int):
        assert tuple(rp.iter_partition(n, n)) == tuple(rp.iter_partition(n))

    def test_max_len_is_1(self, n: int):
        assert tuple(rp.iter_partition(n, 1)) == ([n],)

    def test_max_len_is_2(self, n: int):
        assert tuple(rp.iter_partition(n + 1, 2))[0] == [1, n]

    def test_max_len_same_as_filtering(self, n: int, max_len: int):
        all_perms = list(rp.iter_partition(n))
        sml_perms = list(rp.iter_partition(n, max_len))
        assert sml_perms == [x for x in all_perms if len(x) <= max_len]

    def test_value_error_for_max_len_less_than_1(self):
        with pytest.raises(ValueError):
            _ = tuple(rp.iter_partition(1, 0))
