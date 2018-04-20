# /usr/bin/env python3

import bot_server as server
import logging

from tensorforce.environments import Environment


class DotaEnv(Environment):

    def __init__(self):
        self.action_space = (21,)
        self.observation_space = (172,)
        server.run_app()

    def reset(self):
        return server.get_observation()[0]

    def execute(self, actions):
        state, reward, terminal = server.step(action=actions)
        return state, terminal, reward

    @property
    def states(self):
        return dict(type='float', shape=(172,))

    @property
    def actions(self):
        return dict(
            action_type=dict(type='int', num_actions=5),
            move_vector=dict(type='float', shape=(2,), max_value=150.0, min_value=-150.0),
            creep_index=dict(type='int', num_actions=10),
            ability_index=dict(type='int', num_actions=4)
        )


class DotaEnvironment:
    __slots__ = ['observation_space', 'action_space', 'bot_server_thread', 'logger', 'action_space',
                 'observation_space']

    def __init__(self):
        """
         Action space:
            [0:5] - one-hot action class
            [5:15] - one-hot creep to attack
            [15:19] - one-hot ability index
            [19:21] - movement

         Observation space:
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
