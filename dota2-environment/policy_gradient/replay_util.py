import json
import numpy as np
import math


def read_replay(file='data/replay.json'):
    observations = []
    actions = []
    rewards = []
    with open(file, 'r') as replay:
        lines = replay.readlines()
        steps = list(zip(lines[0::2], lines[1::2]))
        prev = None
        for obs, action in steps:
            obs = json.loads(obs)
            action = json.loads(action)
            observations.append(get_observation(obs))
            actions.append(get_action(action))
            rewards.append(get_reward(obs, prev))
            prev = obs

    return observations, actions, rewards


def get_observation(raw_obs):
    observation = {}
    observation.update(self_info=[
        raw_obs['ourAttackDamage'],
        raw_obs['ourLvl'],
        raw_obs['ourHp'],
        raw_obs['ourMana'],
        raw_obs['ourFacing'],
        int(raw_obs['isOurAbility1Available']),
        int(raw_obs['isOurAbility2Available']),
        int(raw_obs['isOurAbility3Available']),
        int(raw_obs['isOurAbility4Available']),
        raw_obs['ourX'],
        raw_obs['ourY'],
    ])
    observation.update(enemy_info=[
        raw_obs['enemyAttackDamage'],
        raw_obs['enemyLvl'],
        raw_obs['enemyHp'],
        raw_obs['enemyMana'],
        raw_obs['enemyFacing'],
        raw_obs['enemyX'],
        raw_obs['enemyY'],
    ])

    # {"type":1,"hp":5,"maxHp":312,"x":-778,"y":-649,"isVisible":false}
    ally_creeps_data = raw_obs['ourCreeps']
    ally_creeps = []
    for creep in ally_creeps_data:
        ally_creeps.append([
            creep['hp'],
            creep['x'],
            creep['y'],
        ])

    observation.update(ally_creeps=ally_creeps)

    enemy_creeps_data = raw_obs['enemyCreeps']
    enemy_creeps = []
    for creep in enemy_creeps_data:
        enemy_creeps.append([
            creep['hp'],
            creep['x'],
            creep['y'],
        ])

    observation.update(enemy_creeps=enemy_creeps)

    observation.update(tower_info=[
        raw_obs['enemyTowerHp'],
        raw_obs['ourTowerHp'],
    ])

    observation.update(damage_info=[
        raw_obs['timeSinceDamagedByHero'],
        raw_obs['timeSinceDamagedByCreep'],
        raw_obs["timeSinceDamagedByTower"],
    ])

    return vectorize_observation(observation)


def get_move(x, y):
    angle = np.arctan2(y, x)
    if angle < 0:
        angle += 2 * math.pi
    return round((angle / (2 * math.pi)) * 16) % 16


def get_action(action):
    action_type = action['type']
    dx = action['dx']
    dy = action['dy']
    param = action['param']

    result = 0
    if action_type == 0 and dx == 0 and dy == 0:
        # Do nothing
        result = 6
    elif action_type == 0:
        result = get_move(dx, dy)
    elif action_type == 1:
        result = 30
    elif action_type == 2:
        result = 15 + param
    elif action_type == 3:
        result = 25 + param
    elif action_type == 4:
        result = 31

    return result


def get_reward(obs, prev):
    reward = 0
    reward += obs['recentlyKilledCreep'] * 200
    reward += obs['recentlyHitHero'] * 50
    reward += obs['recentlyKilledHero'] * 1000
    if prev is not None:
        reward -= (obs['ourHp'] == 0 and prev['ourHp'] != 0) * 1000


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