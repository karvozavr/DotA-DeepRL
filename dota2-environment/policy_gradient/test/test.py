from policy_gradient.agent import PGAgent

import numpy as np
import unittest


class TestPGAgent(unittest.TestCase):

    def test_smoke(self):
        data = [[1, 2, 0], [1, 2, 1], [1, 2, 1]]
        expected = [[1, 2, 0.75], [1, 2, 1.5], [1, 2, 1]]
        data = PGAgent.discount_rewards(data=data, gamma=0.5)
        self.assertEqual(data, expected)
