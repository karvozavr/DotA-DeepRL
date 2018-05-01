#!/usr/bin/env python3

from dotaenv import DotaEnvironment

import numpy as np

from tensorforce.agents import PPOAgent
from tensorforce.execution import Runner
import os

# Create an environment
env = DotaEnvironment()

network_spec = [
    dict(type='dense', size=172, activation='tanh'),
    dict(type='dense', size=172, activation='tanh'),
    dict(type='dense', size=172, activation='tanh'),
    dict(type='dense', size=172, activation='tanh'),
    dict(type='dense', size=172, activation='tanh'),
    dict(type='dense', size=172, activation='tanh'),
    dict(type='dense', size=172, activation='tanh'),
]

agent = PPOAgent(
    actions=env.actions,
    states=env.states,
    discount=0.99,
    network=network_spec,
)


# Callback function printing episode statistics
def episode_finished(r):
    print("Finished episode {ep} after {ts} timesteps (reward: {reward})".format(ep=r.episode, ts=r.episode_timestep,
                                                                                 reward=r.episode_rewards[-1]))
    agent.save_model('./saved_model/')
    return True


def main():
    global agent
    # Network as list of layers

    # Create the runner
    runner = Runner(agent=agent, environment=env)

    # Start learning
    runner.run(episodes=3000, max_episode_timesteps=300, episode_finished=episode_finished)
    runner.close()

    # Print statistics
    print("Learning finished. Total episodes: {ep}. Average reward of last 100 episodes: {ar}.".format(
        ep=runner.episode,
        ar=np.mean(runner.episode_rewards[-100:]))
    )


if __name__ == '__main__':
    main()
