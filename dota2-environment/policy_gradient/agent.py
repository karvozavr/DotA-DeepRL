import logging

from policy_gradient.replay_buffer import ReplayBuffer
import numpy as np

logger = logging.getLogger('agent')


class PGAgent:
    __slots__ = ('env',
                 'replay_buffer',
                 'network',
                 'episodes',
                 'discount',
                 'eps')

    def __init__(self, environment, network, episodes=100, eps=0.5, discount=0.99):
        self.env = environment()
        self.replay_buffer = ReplayBuffer()
        self.network = network()
        self.episodes = episodes
        self.eps = eps
        self.discount = discount

    def policy_gradient(self):
        for episode in range(self.episodes):
            states, actions, rewards = self.sample_data()
            rewards = np.array(rewards)

            logger.debug('Finished episode {ep} with total reward {rew}.'.format(ep=episode, rew=np.sum(rewards)))

            rewards = self.discount_rewards(rewards=rewards, gamma=self.discount)
            self.replay_buffer.extend(zip(states, actions, rewards))
            self.train_network()

    @staticmethod
    def discount_rewards(rewards, gamma):
        running_add = 0
        for t in reversed(range(0, len(rewards))):
            running_add = running_add * gamma + rewards[t]
            rewards[t] = running_add

        return rewards

    @staticmethod
    def normalize_rewards(rewards):
        pass

    @staticmethod
    def train_network():
        raise NotImplementedError

    def sample_data(self, steps=1000):
        states = []
        actions = []
        rewards = []
        state = self.env.reset()
        for i in range(steps):
            action = self.get_action(state=state)
            state, terminal, reward = self.env.execute(actions=action)
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            if terminal:
                break
        return states, actions, rewards

    @staticmethod
    def get_action(state):
        return []
