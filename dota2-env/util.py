#!/usr/bin/env python3

import numpy as np


class ActionClass:
    ACTION_MOVE = 0
    ACTION_ATTACK_HERO = 1
    ACTION_ATTACK_CREEP = 2
    ACTION_USE_ABILITY = 3


def arg(one_hot_encoded_vector):
    return np.argmax(one_hot_encoded_vector)


# TODO
def action_to_json(action_vector):
    """
    Transform vectorized action to bot-compatible JSON message

    Action space:
            [0:5] - one-hot action class
            [5:15] - one-hot creep to attack
            [15:19] - one-hot ability index
            [19:21] - move coordinates

    :param action_vector: vectorized action
    :return: bot-compatible JSON action message
    """
    action = int(np.argmax(action_vector[0:4]))
    params = []
    if action is 0:
        params.append(float(action_vector[19]))
        params.append(float(action_vector[20]))
    elif action is 1:
        pass
    elif action is 2:
        params.append(int(np.argmax(action_vector[5:15])) + 1)
    elif action is 3:
        params.append(int(np.argmax(action_vector[15:19])) + 1)

    action_response = {
        'action': action,
        'params': params
    }
    return action_response


def action_to_json2(actions_dict):
    """
    Lua indexes starts from 1!

    :param action_vector: vectorized action
    :return: bot-compatible JSON action message
    """

    params = []
    action = int(actions_dict['action_type'])
    if action is 0:
        # move
        params.append(float(actions_dict['move_vector'][0]))
        params.append(float(actions_dict['move_vector'][1]))
    elif action is 1:
        # attack hero
        pass
    elif action is 2:
        # attack creep
        params.append(int(actions_dict['creep_index']) + 1)
    elif action is 3:
        # use ability
        params.append(int(actions_dict['ability_index']) + 1)

    action_response = {
        'action': action,
        'params': params
    }
    return action_response


# TODO
def message_to_observation(observation_message):
    """
    Transform bot observation message to
    :param observation_message:
    :return:
    """
    if observation_message is not None:
        observation = vectorize_observation(observation_message['observation'])
        reward = observation_message['reward']
        done = observation_message['done']
    else:
        observation = []
        reward = 0
        done = True
    return observation, reward, done


def vectorize_observation(observation):
    result = []
    result.extend(observation['self_info'])
    result.extend(observation['enemy_info'])

    creeps = observation['enemy_creeps_info']
    for creep_info in creeps:
        result.extend(creep_info)
    for i in range(max(10 - len(creeps), 0)):
        result.extend([0] * 7)

    creeps = observation['ally_creeps_info']
    for creep_info in creeps:
        result.extend(creep_info)
    for i in range(max(10 - len(creeps), 0)):
        result.extend([0] * 7)

    result.extend(observation['tower_info'])
    result.extend(observation['damage_info'])

    return np.array(result)
