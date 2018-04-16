Action = {}

local bot = GetBot()

local ACTION_MOVE = 0
local ACTION_ATTACK_HERO = 1
local ACTION_ATTACK_CREEP = 2
local ACTION_USE_ABILITY = 3

local ability = {
    bot:GetAbilityByName('nevermore_shadowraze1'),
    bot:GetAbilityByName('nevermore_shadowraze2'),
    bot:GetAbilityByName('nevermore_shadowraze3'),
    bot:GetAbilityByName('nevermore_requiem')
}

--- Move by delta vector.
-- @param delta_vector
--
function move_delta(delta_vector)
    local position = bot:GetLocation()

    position[1] = position[1] + delta_vector[1]
    position[2] = position[2] + delta_vector[2]

    bot:Action_MoveToLocation(position)
end

function attack_hero()
    local enemy_table = GetUnitList(UNIT_LIST_ENEMY_HEROES)
    local enemy
    if enemy_table ~= nil then
        enemy = enemy_table[1]
        Action_AttackUnit(enemy, false)
    end
end

function use_ability(ability_idx)
    local ability = ability[ability_idx]
    if ability:IsFullyCastable() then
        Action_UseAbility(ability)
    end
end

function attack_creep(creep_idx)
    local enemy_creeps = bot:GetNearbyCreeps(1500, true)
    if #enemy_creeps >= creep_idx then
        Actiou_AttackUnit(enemy_creeps[creep_idx])
    end
end

function move_to_position(position_vector)
    bot:Action_MoveToLocation(position_vector)
end

function do_nothing()
    -- Do nothing :)
end

--- Execute given action.
-- @param action_info action info {'action': action id, 'params': action parameters}
function Action.execute_action(action_info)
    local action = action_info['action']
    local action_params = action_info['params']

    if action == ACTION_MOVE then
        -- Consider params[1] params[2] as x, y of delta vector
        move_delta(action_params[1], action_params[2])
    elseif action == ACTION_ATTACK_HERO then
        attack_hero()
    elseif action == ACTION_USE_ABILITY then
        use_ability(action_params[1])
    elseif action == ACTION_ATTACK_CREEP then
        -- TODO
    end
end

return Action;