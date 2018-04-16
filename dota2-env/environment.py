# /usr/bin/env python3

import bot_server as server
import logging


class DotaEnvironment:
    __slots__ = ['observation_space', 'action_space', 'bot_server_thread', 'logger', 'action_space', 'observation_space']

    def __init__(self):
        """
         Action space:
            [0:5] - one-hot action class
            [5:15] - one-hot creep to attack
            [15:19] - one-hot ability index
            [19:21]

         Observation space:
            [
        """
        self.action_space = (21,)
        self.observation_space = (172,)
        self.logger = logging.getLogger('dota2env.environment.DotaEnvironment')
        self.logger.debug('Initializing DotaEnvironment instance.')
        self.bot_server_thread = server.run_app()

    def step(self, action):
        """
        Accepts an action and returns a tuple (observation, reward, done).

        :param action: an action provided by the environment
        :return: observation: agent's observation of the current environment
                 reward (float) : amount of reward returned after previous action
                 done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
        """
        return server.step(action=action)

    def reset(self):
        """
        Resets the state of the environment and returns an initial observation.

        :return: observation: the initial observation of the space.
        """
        return server.get_observation()[0]
