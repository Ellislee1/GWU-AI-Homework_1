import unittest

import numpy as np

import util
from AStar import AStar as A
from Environment import Environment as Env


class EnvironmentTests(unittest.TestCase):
    
    def test_basic(self): 
        # Fill pitcher test
        pitchers = np.array([3])
        goal = 3
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),2)

    def test_0(self):
        # multiple(s) test
        pitchers = np.array([3,4])
        goal = 6
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),4)

    def test_1(self):
        # transfer once test
        pitchers = np.array([2,5])
        goal = 8
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),5)

    def test_2(self):
        # transfer twice test both greater
        pitchers = np.array([5,7])
        goal = 4
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),7)

    def test_3(self):
        # bigger multiple decision test
        pitchers = np.array([3,9])
        goal = 6
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),3)

    def test_4(self): 
        # transfer twice w/ inbetween goal
        pitchers = np.array([3,21])
        goal = 15
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),5) 

    def test_5(self):
        # 3 pitcher test - unused largest
        pitchers = np.array([2,5,7])
        goal = 8
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),5)

    def test_6(self): # 12-5 = 7
        # 3 pitcher test - unused smallest
        pitchers = np.array([1,5,12])
        goal = 7
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),3)
    
    # Needs a new h
    def test_7(self): # 12-3 = 9 + (4-3) = 10
        # 3 pitcher - unused largest
        pitchers = np.array([3,4,12])
        goal = 10
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),6)

    def test_8(self): # 15-3 = 12-1 = 11
        # 4 pitcher - transfer twice same pitcher till goal state
        pitchers = np.array([1,3,15,23])
        goal = 11
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),4)

    def test_9(self): # (31-11) = 20 * 2
        pitchers = np.array([7,11,17,23,31,57])
        goal = 40
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),3)

    def test_10(self): # 6*9 + 4 + 3 
        # 5 pitcher - long time test
        pitchers = np.array([1,2,3,4,6])
        goal = 61
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEquals(a.get_steps(),22)

    def test_11(self):
        # 4 Pitcher - No solution
        pitchers = np.array([2,4,6,8])
        goal = 13
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEquals(a.get_steps(),-1)

    def test_12(self):
        # 4 Pitcher - 2 transfer no dump
        pitchers = np.array([1,4,20,31])
        goal = 27
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEquals(a.get_steps(),3)

    def test_13(self):
        # no step test
        pitchers = np.array([1])
        goal = 0
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEquals(a.get_steps(),0)
    
    def test_14(self):
        # transfer+transfer+dump test
        pitchers = np.array([1,14,31])
        goal = 4
        env = Env(pitchers,goal)
        a = A(env)
        a.run(naive = False)
        self.assertEquals(a.get_steps(),7)

    def test_15(self):
        pitchers = np.array([2,51,99])
        goal = 77
        env = Env(pitchers, goal)
        a = A(env)
        a.run(naive = False)
        self.assertEquals(a.get_steps(),23)

    def test_16(self):
        pitchers = np.array([1,5,7])
        goal = 3
        env = Env(pitchers, goal)
        a = A(env)
        a.run(naive = False)
        self.assertEquals(a.get_steps(),5)

    def test_17(self):
        pitchers = np.array([40,42])
        goal = 10
        env = Env(pitchers, goal)
        a = A(env)
        a.run(naive = False)
        self.assertEqual(a.get_steps(),19)


class UtilTests(unittest.TestCase):
    def test_valid_problems(self):
        self.assertTrue(util.is_valid_problem(np.array([2, 5]), 2))
        self.assertTrue(util.is_valid_problem(np.array([1, 2]), 3))
        self.assertTrue(util.is_valid_problem(np.array([4, 7]), 13))
        self.assertTrue(util.is_valid_problem(np.array([6, 15, 10]), 7))

    def test_invalid_problems(self):
        self.assertFalse(util.is_valid_problem(np.array([3, 6]), 2))
        self.assertFalse( util.is_valid_problem(np.array([2, 4, 6, 8]), 3))
        self.assertFalse( util.is_valid_problem(np.array([6, 15, 12, 9, 24]), 1))
        self.assertFalse( util.is_valid_problem([6], 5))

    def test_closest_pitcher(self):
        closest, index = util.find_closest(np.array([1, 2, 3, 4]), 5)
        self.assertEquals(closest,4)
        self.assertEquals(index,3)

        closest, index = util.find_closest(np.array([15, 10, 5]), 14)
        self.assertEquals(closest,15)
        self.assertEquals(index,0)

        closest, index = util.find_closest(np.array([3, 6]), 4)
        self.assertEquals(closest,3)
        self.assertEquals(index,0)

        closest, index = util.find_closest(np.array([6, 4, 1]), 3)
        self.assertEquals(closest,4)
        self.assertEquals(index,1)

    def test_closest_multiple(self):
        self.assertEquals(util.closest_multiple(4, 12), 3)
        self.assertEquals(util.closest_multiple(1, 5), 5)
        self.assertEquals(util.closest_multiple(4, 3), 1)
        self.assertEquals(util.closest_multiple(5, 1), 0)
        self.assertEquals(util.closest_multiple(7, 10), 1)
        self.assertEquals(util.closest_multiple(7, 12), 2)


if __name__ == "__main__":
    unittest.main()
