#!/usr/bin/env python3
import random
import sys
import time
import numpy as np

from environment import DotaEnvironment
import logging

logger = logging.getLogger('dota2env')
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


def main():
    env = DotaEnvironment()
    obs = env.reset()
    while True:
        a = np.zeros(env.action_space)
        a[0] = 1
        a[-2] = random.choice([random.uniform(-50, -20), random.uniform(20, 50)])
        a[-1] = random.choice([random.uniform(-50, -20), random.uniform(20, 50)])
        obs, reward, done = env.step(action=a)
        print('Observation: {obs}\nReward: {reward}\nDone: {done}'.format(obs=len(obs), reward=reward, done=done))
        # time.sleep(0.01)


if __name__ == '__main__':
    main()
