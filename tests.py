import unittest
from Environment import Environment as Env
import numpy as np

pitchers = np.array([1,5,9,11])

class EnvironmentTests(unittest.TestCase):
    
    def test_fill_source(self):
        env = Env(pitchers,0)
        test_pitchers = np.zeros(len(pitchers)+1)

        # Checking pitcher initilisation
        self.assertTrue( (test_pitchers == env.get_state()).all())

        # Fill the 1 and 9 pitchers to max
        env.fill(-2,0)
        test_pitchers[0] = pitchers[0]
        self.assertTrue(( test_pitchers == env.get_state()).all())
        self.assertEqual(env.steps, 1)

        env.fill(-2,3)
        test_pitchers[3] = pitchers[3]
        self.assertTrue((test_pitchers == env.get_state()).all())
        self.assertEqual(env.steps, 2)

        # Test you can't fill the inf pitcher
        env.fill(-2,-1)
        self.assertTrue((test_pitchers == env.get_state()).all())
        self.assertEqual(env.steps, 2)

    def test_fill_pitcher(self):
        env = Env(pitchers,0)
        test_pitchers = np.zeros(len(pitchers)+1)
        test_pitchers[1] = pitchers[1]
        env.fill(-2,1)
        test_pitchers[3] = pitchers[3]
        env.fill(-2,3)

        # Checking pitcher initilisation
        self.assertTrue( (test_pitchers == env.get_state()).all())

        # Check moving volumes around the pitchers
        env.fill(1,-1)
        test_pitchers[-1], test_pitchers[1] = 5,0

        self.assertTrue( (test_pitchers == env.get_state()).all())
        self.assertEqual(env.steps, 3)

        env.fill(-1,2)
        test_pitchers[2], test_pitchers[-1] = 5,0

        self.assertTrue( (test_pitchers == env.get_state()).all())
        self.assertEqual(env.steps, 4)

         # Test pitchers don't overflow
        env.fill(3,0)
        test_pitchers[0], test_pitchers[3] = 1,10

        self.assertTrue( (test_pitchers == env.get_state()).all())
        self.assertEqual(env.steps, 5)

        # Test pitchers don't underflow
        env.fill(-1,2)
        self.assertTrue( (test_pitchers == env.get_state()).all())
        self.assertEqual(env.steps, 5)

if __name__ == '__main__':
    unittest.main()