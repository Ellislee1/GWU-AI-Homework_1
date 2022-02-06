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


if __name__ == "__main__":
    test_valid_problems()
    test_invalid_problems()
