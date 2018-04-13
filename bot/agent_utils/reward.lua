local Constant = require(GetScriptDirectory()..'/dev/constant_each_side')
local DotaBotUtility = require(GetScriptDirectory()..'/utility')

Reward = {}

local LastEnemyHP = 1000

local EnemyTowerPosition = Vector(1024,320)
local AllyTowerPosition = Vector(-1656,-1512)

local LastEnemyTowerHP = 1300

local LastDecesion = -1000

local LastKill = 0

local LastDeath = 0

local LastXPNeededToLevel = 0

local DeltaTime = 300 / 2

local GotOrder = false

local creep_zero_padding = {0,0,0,0,0,0,0}

local first = "true"

local punish = 0

local vec_delta = Vector(0,0,0)

local map_div = 7000

local msg_done = false

local seq_num = 0

function Reward.get_reward()
	local npcBot = GetBot()
    local enemyBotTbl = GetUnitList(UNIT_LIST_ENEMY_HEROES)
    local enemyBot = nil
    if enemyBotTbl ~= nil then
        enemyBot = enemyBotTbl[1]
    end

    local myid = npcBot:GetPlayerID()

    local MyKill = GetHeroKills(myid)
    local MyDeath = GetHeroDeaths(myid)

    if(enemyBot ~= nil) then 
        npcBot:SetTarget(enemyBot)
    end
    local enemyTower = GetTower(TEAM_DIRE, TOWER_MID_1);
    local AllyTower = GetTower(TEAM_RADIANT, TOWER_MID_1);

    if MyLastGold == nil then
        MyLastGold = npcBot:GetGold()
    end

    local GoldReward = 0

    if npcBot:GetGold() - MyLastGold > 5 then
        GoldReward = (npcBot:GetGold() - MyLastGold)
    end

    local _XPNeededToLevel = npcBot:GetXPNeededToLevel()

    local XPreward = 0

    if _XPNeededToLevel < LastXPNeededToLevel then
        XPreward = LastXPNeededToLevel - _XPNeededToLevel
    end

    if MyLastHP == nil then
        MyLastHP = npcBot:GetHealth()
    end

    if LastEnemyHP == nil then
        LastEnemyHP = 600
    end

    if LastDistanceToEnemy == nil then
        LastDistanceToEnemy = 2000
    end

    if LastEnemyMaxHP == nil then
        LastEnemyMaxHP = 1000
    end
    
    if(enemyBot ~= nil) then 
        EnemyHP = enemyBot:GetHealth()
        EnemyMaxHP = enemyBot:GetMaxHealth()
    else
        
        EnemyHP = 600
        EnemyMaxHP = 1000
    end

    if(enemyBot ~= nil and enemyBot:CanBeSeen()) then
        DistanceToEnemy = GetUnitToUnitDistance(npcBot,enemyBot)
        if(DistanceToEnemy > 2000) then
            DistanceToEnemy = 2000
        end
    else
        DistanceToEnemy = LastDistanceToEnemy
    end

    if EnemyHP < 0 then
        EnemyHP = LastEnemyHP
        EnemyMaxHP = LastEnemyMaxHP
    end

    if AllyTowerLastHP == nil then
        AllyTowerLastHP = AllyTower:GetHealth()
    end

    if enemyTower:GetHealth() > 0 then
        EnemyTowerHP = enemyTower:GetHealth()
    else
        EnemyTowerHP = LastEnemyTowerHP
    end
    local AllyLaneFront = GetLaneFrontLocation(DotaBotUtility:GetEnemyTeam(), LANE_MID, 0)
    local EnemyLaneFront = GetLaneFrontLocation(TEAM_RADIANT,LANE_MID,0)

    local DistanceToEnemyLane = GetUnitToLocationDistance(npcBot,EnemyLaneFront)
    local DistanceToAllyLane = GetUnitToLocationDistance(npcBot,AllyLaneFront)

    local DistanceToEnemyTower = GetUnitToLocationDistance(npcBot,EnemyTowerPosition)
    local DistanceToAllyTower = GetUnitToLocationDistance(npcBot,AllyTowerPosition)

    local DistanceToLane = (DistanceToEnemyLane + DistanceToAllyLane) / 2

    if LastDistanceToLane == nil then
        LastDistanceToLane = DistanceToLane
    end

    if(LastEnemyLocation == nil) then
        if(GetTeam() == TEAM_RADIANT) then
            LastEnemyLocation = Vector(6900,6650)
        else
            LastEnemyLocation = Vector(-7000,-7000)
        end
    end

    local EnemyLocation = Vector(0,0)
    if(enemyBot~=nil) then
        EnemyLocation = enemyBot:GetLocation()
    else
        EnemyLocation = LastEnemyLocation
    end
    
    local MyLocation = npcBot:GetLocation()

    local BotTeam = 0
    if(GetTeam() == TEAM_RADIANT) then
        BotTeam = 1
    else
        BotTeam = -1
    end

    if npcBot:DistanceFromFountain() == 0 and npcBot:GetHealth() == npcBot:GetMaxHealth() then
        punish = punish + 5
    end

    local EnemyHPReward = 0
    if (EnemyHP - LastEnemyHP) < 0 then
        EnemyHPReward = (EnemyHP - LastEnemyHP)-- * 2
    end

    local dist2line = PointToLineDistance(Vector(8000,8000), Vector(-8000,-8000), MyLocation)["distance"]

    local distance2mid = 0.1 * math.sqrt(MyLocation[1]*MyLocation[1] + MyLocation[2] * MyLocation[2])
        + dist2line
    
    -- print("dist2line", dist2line)

    if MyLastDistance2mid == nil then
        MyLastDistance2mid = distance2mid
    end

    local reward = (npcBot:GetHealth() - MyLastHP) / 10.0
    --- EnemyHPReward
    -- + (MyKill - LastKill) * 100
    - (MyDeath - LastDeath) * 100
    -- + GoldReward
    + XPreward / 10.0
    --- punish
    - (MyLastDistance2mid - distance2mid) / 100.0
    -0.01

    if enemyTower:GetHealth() > 0 then
        LastEnemyTowerHP = enemyTower:GetHealth()
    end

    MyLastHP = npcBot:GetHealth()
    AllyTowerLastHP = AllyTower:GetHealth()
    LastEnemyHP = EnemyHP
    LastEnemyMaxHP = EnemyMaxHP
    MyLastGold = npcBot:GetGold()
    LastDistanceToLane = DistanceToLane
    LastDistanceToEnemy = DistanceToEnemy
    LastEnemyLocation = EnemyLocation
    LastKill = MyKill
    LastDeath = MyDeath
    LastXPNeededToLevel = _XPNeededToLevel
    MyLastDistance2mid = distance2mid
    punish = 0

    return reward
end

return Reward;