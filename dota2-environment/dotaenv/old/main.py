#!/usr/bin/env python3

import random
import sys
import time
import numpy as np

from environment import DotaEnv
import logging

logger = logging.getLogger('dota2env')
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


def main():
    env = DotaEnv()
    obs = env.reset()
    while True:
        a = dict(
            action_type=0,
            move_vector=(55, 55)
        )

        obs, terminal, reward = env.execute(actions=a)
        if terminal:
            print('Observation: {obs}\nReward: {reward}\nDone: {done}'.format(obs=len(obs), reward=reward, done=terminal))
            obs = env.reset()
        # time.sleep(0.01)


if __name__ == '__main__':
    main()
