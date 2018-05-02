from policy_gradient.agent import PGAgent

import numpy as np
from numpy.testing import *
import unittest


class TestPGAgent(unittest.TestCase):

    def test_smoke(self):
        data = np.array([0, 1, 1], dtype='float32')
        expected = np.array([0.75, 1.5, 1], dtype='float32')
        data = PGAgent.discount_rewards(rewards=data, gamma=0.5)
        self.assertTrue(np.allclose(data, expected))
