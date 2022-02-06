import util
import numpy as np


def test_valid_problems():
    assert util.is_valid_problem(np.array([2, 5]), 2)
    assert util.is_valid_problem(np.array([1, 2]), 3)
    assert util.is_valid_problem(np.array([4, 7]), 13)
    assert util.is_valid_problem(np.array([6, 15, 10]), 7)


def test_invalid_problems():
    assert util.is_valid_problem(np.array([3, 6]), 2) == False
    assert util.is_valid_problem(np.array([2, 4, 6, 8]), 3) == False
    assert util.is_valid_problem(np.array([6, 15, 12, 9, 24]), 1) == False


def test_closest_pitcher():
    closest, index = util.find_closest(np.array([1, 2, 3, 4]), 5)
    assert closest == 4 and index == 3

    closest, index = util.find_closest(np.array([15, 10, 5]), 14)
    assert closest == 15 and index == 0

    closest, index = util.find_closest(np.array([3, 6]), 4)
    assert closest == 3 and index == 0

    closest, index = util.find_closest(np.array([6, 4, 1]), 3)
    assert closest == 4 and index == 1


def test_closest_multiple():
    assert util.closest_multiple(4, 12) == 3
    assert util.closest_multiple(1, 5) == 5
    assert util.closest_multiple(4, 3) == 1
    assert util.closest_multiple(5, 1) == 0
    assert util.closest_multiple(7, 10) == 1
    assert util.closest_multiple(7, 12) == 2


if __name__ == "__main__":
    test_valid_problems()
    test_invalid_problems()
    test_closest_pitcher()
    test_closest_multiple()
