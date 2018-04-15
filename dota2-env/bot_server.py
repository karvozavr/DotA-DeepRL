#!/usr/bin/env python3
from enum import IntEnum
from threading import Event, Thread, RLock
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


def run_app():
    app_thread = Thread(target=app.run)
    app_thread.setDaemon(True)
    app_thread.start()


class FsmState(IntEnum):
    WHAT_NEXT = 0
    ACTION_RECEIVED = 1
    SEND_OBSERVATION = 2


lock = RLock
observation_received = Event()
observation = None
current_fsm_state = FsmState.WHAT_NEXT


def get_observation():
    """
    Get observation from bot.

    :return: tuple (observation, reward, is_done)
    """
    global current_fsm_state
    lock.acquire()
    current_fsm_state = FsmState.SEND_OBSERVATION
    lock.release()

    observation_received.wait()
    result = observation
    observation_received.clear()

    obs = result['observation']
    reward = result['reward']
    done = result['done']
    return obs, reward, done


def decide_what_next():
    lock.acquire()
    result = current_fsm_state
    lock.release()
    return result


def bot_response(fsm_state, action=None):
    return jsonify({'fsm_state': fsm_state, 'action': action})


@app.route('/observation', methods=['POST'])
def process_observation():
    global observation
    response = ''
    if request.method == 'POST':
        observation = request.get_json()['content']
        observation_received.set()
        response = bot_response(FsmState.WHAT_NEXT)
    return response


@app.route('/what_next', methods=['POST'])
def process_what_next():
    response = ''
    if request.method == 'POST':
        print(request.get_json())
        response = bot_response(decide_what_next())
    return response


if __name__ == '__main__':
    run_app()
