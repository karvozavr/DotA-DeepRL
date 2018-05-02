import logging

from policy_gradient.replay_buffer import ReplayBuffer
from policy_gradient.network import Network
import numpy as np
import random
from sklearn.preprocessing import OneHotEncoder

logger = logging.getLogger('PGAgent')

input_shape = 172
output_shape = 32


class PGAgent:
    """
    Policy gradient agent.
    """
    __slots__ = ('env',
                 'replay_buffer',
                 'network',
                 'episodes',
                 'discount',
                 'batch_size',
                 'eps')

    def __init__(self, environment, episodes=100, batch_size=100, eps=0.7, discount=0.99):
        self.env = environment()
        self.replay_buffer = ReplayBuffer()
        self.network = Network(input_shape=input_shape, output_shape=output_shape)
        self.episodes = episodes
        self.batch_size = batch_size
        self.eps = eps
        self.discount = discount

    def train(self):
        for episode in range(self.episodes):
            # sample data
            states, actions, rewards = self.sample_data()
            rewards = np.array(rewards)

            logger.info('Finished episode {ep} with total reward {rew}.'.format(ep=episode, rew=np.sum(rewards)))

            # discount and normalize rewards
            rewards = self.discount_rewards(rewards=rewards, gamma=self.discount)
            rewards = self.normalize_rewards(rewards=rewards)

            # extend replay buffer with sampled data
            self.replay_buffer.extend(zip(states, actions, rewards))

            # update epsilon
            self.update_eps(coefficient=0.95)

            # if there are enough data in replay buffer, train the model on it
            if len(self.replay_buffer) >= self.batch_size:
                self.train_network()

        logger.info('Finished training.')

    def sample_data(self, steps=100):
        states = []
        actions = []
        rewards = []
        state = self.env.reset()
        for i in range(steps):
            action = self.get_action(state=state, eps=self.eps)
            state, terminal, reward = self.env.execute(action=action)
            logger.info('Step {step} reward is {rew}.'.format(step=i, rew=reward))
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            if terminal:
                break
        return states, actions, rewards

    def get_action(self, state, eps):
        """
        Get action by epsilon-greedy strategy.
        :param state: state
        :return: action
        """
        if random.uniform(0, 1) > eps:
            return self.network.predict(state=state)
        else:
            return random.randint(0, output_shape - 1)

    @staticmethod
    def discount_rewards(rewards, gamma):
        """
        Discount rewards backwards.
        :param rewards: rewards numpy array
        :param gamma: discount factor
        :return: discounted rewards array
        """
        running_add = 0.
        for t in reversed(range(0, len(rewards))):
            running_add = running_add * gamma + rewards[t]
            np.put(a=rewards, ind=t, v=running_add)

        return rewards

    @staticmethod
    def normalize_rewards(rewards):
        mean = np.mean(rewards)
        std = np.std(rewards)
        rewards -= mean
        rewards /= std
        return rewards

    def update_eps(self, coefficient=0.9):
        self.eps *= coefficient

    def train_network(self):
        states, actions, rewards = self.replay_buffer.get_data(self.batch_size)
        states = np.array(states)

        enc = OneHotEncoder(n_values=output_shape)
        actions = np.array(actions).reshape(-1, 1)
        actions = enc.fit_transform(actions).toarray()

        rewards = np.array(rewards, dtype='float32')

        logger.info('Training network on batch: states {s_shape}, actions {a_shape}, rewards {r_shape}.'
                    .format(s_shape=states.shape, a_shape=actions.shape, r_shape=rewards.shape))

        self.network.train(states=states, actions=actions, rewards=rewards)
