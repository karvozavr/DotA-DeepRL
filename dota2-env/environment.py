# /usr/bin/env python3
import threading

import bot_server as server


class DotaEnvironment():
    observation_space = None
    action_space = None

    def __init__(self):
        server.run_app()

    def step(self, action):
        """
        Accepts an action and returns a tuple (observation, reward, done).

        :param action: an action provided by the environment
        :return: observation: agent's observation of the current environment
                 reward (float) : amount of reward returned after previous action
                 done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
        """
        raise NotImplementedError

    def reset(self):
        """
        Resets the state of the environment and returns an initial observation.

        :return: observation: the initial observation of the space.
        """
        raise NotImplementedError
