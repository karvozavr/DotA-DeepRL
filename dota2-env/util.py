#!/usr/bin/env python3

from flask import jsonify


# TODO
def action_to_json(action):
    """
    Transform vectorized action to bot-compatible JSON message

    :param action: vectorized action
    :return: bot-compatible JSON action message
    """
    action_response = jsonify({'action': action, 'params': [1, 2, 3, 4, 5]})
    return action_response


# TODO
def message_to_observation(observation_message):
    """
    Transform bot observation message to
    :param observation_message:
    :return:
    """
    observation = observation_message['observation']
    reward = observation_message['reward']
    done = observation['done']
    return observation, reward, done
