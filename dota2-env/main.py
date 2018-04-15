#!/usr/bin/env python3
import sys
import time

from environment import DotaEnvironment
import logging

logger = logging.getLogger('dota2env')
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


def main():
    env = DotaEnvironment()
    obs, reward, done = env.reset()
    while True:
        obs, reward, done = env.step(action=66)
        #print('Observation: {obs}\nReward: {reward}\nDone: {done}'.format(obs=obs, reward=reward, done=done))
        time.sleep(0.01)


if __name__ == '__main__':
    main()
