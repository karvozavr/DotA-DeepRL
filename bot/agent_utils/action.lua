Action = {}

local bot = GetBot()

local ACTION_MOVE = 0
local ACTION_ATTACK_HERO = 1
local ACTION_ATTACK_CREEP = 2
local ACTION_USE_ABILITY = 3
local ACTION_ATTACK_TOWER = 4
local last_time_move = GameTime()

local ABILITY = {
    bot:GetAbilityByName('nevermore_shadowraze1'),
    bot:GetAbilityByName('nevermore_shadowraze2'),
    bot:GetAbilityByName('nevermore_shadowraze3'),
    bot:GetAbilityByName('nevermore_requiem')
}

function Action.last_time_moved()
    if last_time_move == nil then
        last_time_move = GameTime()
    end
    return last_time_move
end

--- Move by delta vector.
-- @param delta_vector
--
function move_delta(delta_vector)
    local position = bot:GetLocation()

    last_time_move = GameTime()

    print('MOVE', delta_vector[1], delta_vector[2])
    position[1] = position[1] + delta_vector[1]
    position[2] = position[2] + delta_vector[2]

    bot:Action_MoveDirectly(position)
end

--- Attack enemy hero.
--
function attack_hero()
    print('ATTACK HERO')
    local enemy_table = GetUnitList(UNIT_LIST_ENEMY_HEROES)
    local enemy
    if #enemy_table > 0 then
        enemy = enemy_table[1]
        bot:Action_AttackUnit(enemy, false)
    end
end

--- Use ability.
-- @param ability_idx index of ability in 'ABILITY' table.
--
function use_ability(ability_idx)
    print('USE ABILITY', ability_idx)
    local ability = ABILITY[ability_idx]
    if ability:IsFullyCastable() then
        bot:Action_UseAbility(ability)
    end
end

--- Attack enemy creep.
-- @param creep_idx index of creep in nearby creeps table.
--
function attack_creep(creep_idx)
    print('ATTACK CREEP', creep_idx)
    local enemy_creeps = bot:GetNearbyCreeps(1500, true)
    if #enemy_creeps >= creep_idx then
        bot:Action_AttackUnit(enemy_creeps[creep_idx], false)
    end
end

function attack_tower()
    print('ATTACK TOWER')
    local towers = bot:GetNearbyTowers(1500, true)
    if #towers > 0 then
        bot:Action_AttackUnit(towers[1], false)
    end
end

function move_to_position(position_vector)
    bot:Action_MoveToLocation(position_vector)
end

function upgrade_abilities()
    bot:ActionImmediate_LevelAbility('nevermore_shadowraze1')
end

--- Execute given action.
-- @param action_info action info {'action': action id, 'params': action parameters}
--
function Action.execute_action(action_info)
    local action = action_info['action']
    local action_params = action_info['params']

    upgrade_abilities()

    if action == ACTION_MOVE then
        -- Consider params[1], params[2] as x, y of delta vector
        move_delta(action_params)
    elseif action == ACTION_ATTACK_HERO then
        attack_hero()
    elseif action == ACTION_USE_ABILITY then
        -- Consider params[1] as ability index
        use_ability(action_params[1])
    elseif action == ACTION_ATTACK_CREEP then
        -- Consider params[1] as index in nearby creeps table
        attack_creep(action_params[1])
    elseif action == ACTION_ATTACK_TOWER then
        attack_tower()
    end
end

return Action;