#!/usr/bin/env python3

from policy_gradient import PGAgent
from dotaenv import DotaEnvironment
from policy_gradient import replay_util
import logging

logger = logging.getLogger('DotaRL')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log/policy_gradient.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def create_dota_agent():
    return PGAgent(environment=DotaEnvironment,
                   episodes=500,
                   batch_size=500,
                   eps=0.7,
                   discount=0.99,
                   eps_update=0.95)


def main():
    # logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(message)s')
    # agent = create_dota_agent()
    # agent.train()
    print(replay_util.read_replay()[0:5])


if __name__ == '__main__':
    main()
