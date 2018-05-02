#!/usr/bin/env python3

from policy_gradient import PGAgent
from dotaenv import DotaEnvironment


def create_dota_agent():
    return PGAgent(environment=DotaEnvironment)


def main():
    agent = create_dota_agent()
    agent.train()


if __name__ == '__main__':
    main()
