#!/usr/bin/env python

import numpy as np
import scipy.special
from dotaenv import DotaEnvironment


def include_bias(x):
    # Add a constant term (1.0) to each entry in x
    return np.concatenate([x, np.ones_like(x[..., :1])], axis=-1)


def log_softmax(logits):
    return logits - scipy.special.logsumexp(logits, axis=-1, keepdims=True)


def point_get_logp_action(theta, ob, action):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :param action: A vector of size |A|
    :return: A scalar
    """
    ob_1 = include_bias(ob)
    mean = theta.dot(ob_1)
    zs = action - mean
    return -0.5 * np.log(2 * np.pi) * theta.shape[0] - 0.5 * np.sum(np.square(zs))


def point_get_grad_logp_action(theta, ob, action):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :param action: A vector of size |A|
    :return: A matrix of size |A| * (|S|+1)
    """

    ob_1 = include_bias(ob)
    mean = np.dot(theta, ob_1)
    grad = np.outer(action - mean, ob_1)

    return grad


def point_get_action(theta, ob, rng=np.random):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :return: A vector of size |A|
    """
    ob_1 = include_bias(ob)
    mean = theta.dot(ob_1)
    return rng.normal(loc=mean, scale=1.)


def compute_entropy(logits):
    """
    :param logits: A matrix of size N * |A|
    :return: A vector of size N
    """
    logp = log_softmax(logits)
    return -np.sum(logp * np.exp(logp), axis=-1)


def main():
    # Check gradient implementation

    n_itrs = 10000
    env = DotaEnvironment()
    rng = np.random.RandomState(42)
    timestep_limit = 10000
    learning_rate = 0.1
    discount = 0.99

    batch_size = 100
    # Initialize parameters
    theta = rng.normal(scale=0.2, size=(env.action_space[0], env.observation_space[0] + 1))

    # Store baselines for each time step.
    baselines = np.zeros(timestep_limit)

    # Policy training loop
    for itr in range(n_itrs):
        # Collect trajectory loop
        n_samples = 0
        grad = np.zeros_like(theta)
        episode_rewards = []

        # Store cumulative returns for each time step
        all_returns = [[] for _ in range(timestep_limit)]

        all_observations = []
        all_actions = []

        while n_samples < batch_size:
            observations = []
            actions = []
            rewards = []
            ob = env.reset()
            done = False
            # Collect a new trajectory
            print('collecting')
            print(n_samples, batch_size)
            while not done:
                action = point_get_action(theta, ob, rng=rng)
                next_ob, rew, done = env.step(action)
                observations.append(ob)
                actions.append(action)
                rewards.append(rew)
                ob = next_ob
                n_samples += 1
            # Go back in time to compute returns and accumulate gradient
            # Compute the gradient along this trajectory
            R = 0.
            for t in reversed(range(len(observations))):
                def compute_update(discount, R_tplus1, theta, s_t, a_t, r_t, b_t, get_grad_logp_action):
                    """
                    :param discount: A scalar
                    :param R_tplus1: A scalar
                    :param theta: A matrix of size |A| * (|S|+1)
                    :param s_t: A vector of size |S|
                    :param a_t: Either a vector of size |A| or an integer, depending on the environment
                    :param r_t: A scalar
                    :param b_t: A scalar
                    :param get_grad_logp_action: A function, mapping from (theta, ob, action) to the gradient (a
                    matrix of size |A| * (|S|+1) )
                    :return: A tuple, consisting of a scalar and a matrix of size |A| * (|S|+1)
                    """
                    R_t = discount * R_tplus1 + r_t
                    A_t = R_t - b_t
                    pg_theta = get_grad_logp_action(theta, s_t, a_t) * A_t

                    return R_t, pg_theta

                R, grad_t = compute_update(
                    discount=discount,
                    R_tplus1=R,
                    theta=theta,
                    s_t=observations[t],
                    a_t=actions[t],
                    r_t=rewards[t],
                    b_t=baselines[t],
                    get_grad_logp_action=point_get_grad_logp_action
                )
                all_returns[t].append(R)
                grad += grad_t

            episode_rewards.append(np.sum(rewards))
            all_observations.extend(observations)
            all_actions.extend(actions)

        baselines = np.zeros(timestep_limit)

        # Roughly normalize the gradient
        grad = grad / (np.linalg.norm(grad) + 1e-8)

        theta += learning_rate * grad

        print("Iteration: %d AverageReturn: %.2f |theta|_2: %.2f" % (
        itr, np.mean(episode_rewards), np.linalg.norm(theta)))


if __name__ == "__main__":
    main()
