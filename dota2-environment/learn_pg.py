#!/usr/bin/env python3

from policy_gradient import PGAgent
from dotaenv import DotaEnvironment
from policy_gradient import replay_util
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DotaRL')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log/policy_gradient.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def create_dota_agent():
    return PGAgent(environment=DotaEnvironment,
                   episodes=500,
                   batch_size=500,
                   eps=0.4,
                   discount=0.99,
                   eps_update=0.95)


def main():
    agent = create_dota_agent()
    # agent.train_on_replay(epochs=100000, batch_size=1000)
    agent.train()


if __name__ == '__main__':
    main()
