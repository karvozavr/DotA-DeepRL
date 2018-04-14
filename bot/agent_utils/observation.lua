-- Observation module
local Observation = {}

local bot = GetBot()

local ability1 = bot:GetAbilityByName('nevermore_shadowraze1')
local ability2 = bot:GetAbilityByName('nevermore_shadowraze2')
local ability3 = bot:GetAbilityByName('nevermore_shadowraze3')
local ability4 = bot:GetAbilityByName('nevermore_requiem')

local creep_zero_padding = {0, 0, 0, 0, 0, 0, 0}

-- Obtain team info.
local function get_team()
    if (GetTeam() == TEAM_RADIANT) then
        return 1
    else
        return -1
    end
end

-- Obtain damage info.
function get_damage_info()
    local damage_info = {
        bot:TimeSinceDamagedByAnyHero(),
        bot:TimeSinceDamagedByCreep(),
        bot:TimeSinceDamagedByTower(),
    }
end

-- Obtain towers info.
function get_towers_info()
    local enemy_tower = GetTower(TEAM_DIRE, TOWER_MID_1);
    local ally_tower = GetTower(TEAM_RADIANT, TOWER_MID_1);
    if get_team() == -1 then
        local temp = ally_tower
        ally_tower = enemy_tower
        enemy_tower = temp
    end
        
    local enemy_tower_info = { enemy_tower:GetMaxHealth(), enemy_tower:GetHealth() }
    local ally_tower_info = { ally_tower:GetMaxHealth(), ally_tower:GetHealth() }

    return {enemy_tower_info, ally_tower_info}
end

-- Obtain bot's info (specified for Nevermore).
function get_self_info()
    local ability1_dmg = 0
    if ability1:IsFullyCastable() then
        ability1_dmg = ability1:GetAbilityDamage()
    end

    local ability2_dmg = 0
    if ability2:IsFullyCastable() then
        ability2_dmg = ability2:GetAbilityDamage()
    end

    local ability3_dmg = 0
    if ability3:IsFullyCastable() then
        ability3_dmg = ability3:GetAbilityDamage()
    end

     local ability4_dmg = 0
    if ability4:IsFullyCastable() then
        ability4_dmg = ability4:GetAbilityDamage()
    end

    -- Bot's atk, hp, mana, abilities, position x, position y
    local self_position = bot:GetLocation()
    local self_info = {
        bot:GetAttackDamage(),
        bot:GetAttackSpeed(),
        bot:GetLevel(),
        bot:GetHealth(),
        bot:GetMaxHealth(),
        bot:GetMana(),
        bot:GetMaxMana(),
        bot:GetFacing(),
        ability1_dmg,
        ability2_dmg,
        ability3_dmg,
        ability4_dmg,
        bot:DistanceFromFountain(),
        self_position[1],
        self_position[2]
    }

    return self_info
end

-- Obtain enemy hero info.
function get_enemy_info()
	local enemy_table = GetUnitList(UNIT_LIST_ENEMY_HEROES)
    local enemy
    if enemy_table ~= nil then
        enemy = enemy_table[1]
    end

    local enemy_hero_input = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
    if(enemy ~= nil) then
        local enemy_position = enemy:GetLocation()
        enemy_hero_input = {
            enemy:GetAttackDamage(),
            enemy:GetAttackSpeed(),
            enemy:GetLevel(),
            enemy:GetHealth(),
            enemy:GetMaxHealth(),
            enemy:GetMana(),
            enemy:GetMaxMana(),
            enemy:GetFacing(),
            enemypos[1] / map_div,
            enemypos[2] / map_div
        }
    end

    return enemy_hero_input
end

-- Obtain creeps info.
function get_creeps_info(creeps)
    local creeps_info = {}

    if (creeps == nil) then
        table.insert(creeps_info, creep_zero_padding)
        return creeps_info
    end

    for creep_key, creep in pairs(creeps)
    do 
        local position = creep:GetLocation()
        table.insert(creeps_info, {
            creep:GetAttackDamage(),
            creep:GetHealth(),
            creep:GetMaxHealth(),
            creep:GetArmor(),
            creep:GetAttackRange(),
            position[1],
            position[2]
        })
    end

    -- if creeps_info is empty:
    if #creeps_info == 0 then
        table.insert(creeps_info, creep_zero_padding)
    end

    return creeps_info
end

-- Get whole observation.
function Observation.get_observation()
    local observation = {}

    local enemy_creeps = get_creeps_info(bot:GetNearbyCreeps(1000, true))
    local ally_creeps = get_creeps_info(bot:GetNearbyCreeps(1000, false))

    observation = {
        ['self_info'] = get_self_info(),
        ['enemy_info'] = get_enemy_info(),
        ['enemy_creeps_info'] = enemy_creeps,
        ['ally_creeps_info'] = ally_creeps,
        ['tower_info'] = get_towers_info(),
        ['damage_info'] = get_damage_info(),
    }

    return observation
end

return Observation;
