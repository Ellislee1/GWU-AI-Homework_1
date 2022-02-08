import unittest
import numpy as np
from AStar import AStar as A
from Environment import Environment as Env


class EnvironmentTests(unittest.TestCase):
    
    def test_basic(self): 
        # Fill pitcher test
        pitchers = np.array([3])
        goal = 3
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),2)

    def test_0(self):
        # multiple(s) test
        pitchers = np.array([3,4])
        goal = 6
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),4)

    def test_1(self):
        # transfer once test
        pitchers = np.array([2,5])
        goal = 8
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),5)

    def test_2(self):
        # transfer twice test both greater
        pitchers = np.array([5,7])
        goal = 4
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),7)

    def test_3(self):
        # bigger multiple decision test
        pitchers = np.array([3,9])
        goal = 6
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),4)

    def test_4(self): 
        # transfer twice w/ inbetween goal
        pitchers = np.array([3,21])
        goal = 15
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),5) 

    def test_5(self):
        # 3 pitcher test - unused largest
        pitchers = np.array([2,5,7])
        goal = 8
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),5)

    def test_6(self): # 12-5 = 7
        # 3 pitcher test - unused smallest
        pitchers = np.array([1,5,12])
        goal = 7
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),3)
    
    # Needs a new h
    def test_7(self): # 12-3 = 9 + (4-3) = 10
        # 3 pitcher - unused largest
        pitchers = np.array([3,4,12])
        goal = 10
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),6)

    def test_8(self): # 15-3 = 12-1 = 11
        # 4 pitcher - transfer twice same pitcher till goal state
        pitchers = np.array([1,3,15,23])
        goal = 11
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEqual(a.get_steps(),4)

    def test_9(self): # (31-11) = 20 * 2
       pitchers = np.array([7,11,17,23,31,57])
       goal = 40
       env = Env(pitchers,goal)
       a = A(env)
       a.run(naive = True)
       self.assertEqual(a.get_steps(),4)

    def test_10(self): # 6*9 + 4 + 3 
       # 5 pitcher - long time test
       pitchers = np.array([1,2,3,4,6])
       goal = 61
       env = Env(pitchers,goal)
       a = A(env)
       a.run(naive = True)
       self.assertEquals(a.get_steps(),22)

    def test_11(self):
        # 4 Pitcher - No solution
        pitchers = np.array([2,4,6,8])
        goal = 13
        env = Env(pitchers,goal)
        a = A(env)
        a.run()
        self.assertEquals(a.get_steps(),-1)


if __name__ == "__main__":
    unittest.main()
