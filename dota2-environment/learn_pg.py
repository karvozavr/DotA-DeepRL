#!/usr/bin/env python3

from policy_gradient import PGAgent, ReplayBuffer, Network
from dotaenv import DotaEnvironment


def create_dota_agent():
    return PGAgent(environment=DotaEnvironment, network=Network)


def learn():
    raise NotImplementedError


def main():
    raise NotImplementedError


if __name__ == '__main__':
    main()
