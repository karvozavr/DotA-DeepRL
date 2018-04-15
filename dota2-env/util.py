#!/usr/bin/env python3

from flask import jsonify


# TODO
def action_to_json(action):
    action_response = {'action': action, 'params': [1, 2, 3, 4, 5]}
    return action_response


# TODO
def message_to_observation(observation_message):
    observation = observation_message
    return observation
