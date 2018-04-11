local Constant = require(GetScriptDirectory().."/dev/constant_each_side");
local DotaBotUtility = require(GetScriptDirectory().."/utility");

local STATE_IDLE = "STATE_IDLE";
local STATE_ATTACKING_CREEP = "STATE_ATTACKING_CREEP";
local STATE_KILL = "STATE_KILL";
local STATE_RETREAT = "STATE_RETREAT";
local STATE_FARMING = "STATE_FARMING";
local STATE_GOTO_COMFORT_POINT = "STATE_GOTO_COMFORT_POINT";
local STATE_FIGHTING = "STATE_FIGHTING";
local STATE_RUN_AWAY = "STATE_RUN_AWAY";
local STATE_TEAM_FIGHTING = "STATE_TEAM_FIGHTING";
LANE = LANE_MID;

if (true) then
math.randomseed(RealTime())

_G.LaningDesire = math.random()

function GetDesire()
    return _G.LaningDesire
end

end

function OnStart()
    _G.state = "laning"
end

local function IsTowerAttackingMe()
    local npcBot = GetBot();
    if(npcBot:TimeSinceDamagedByTower() < 2) then
        return true;
    else
        return false;
    end
end

local function ConsiderAttackCreeps(StateMachine)
    -- there are creeps try to attack them --
    --print("ConsiderAttackCreeps");
    local npcBot = GetBot();

    local EnemyCreeps = npcBot:GetNearbyCreeps(1600,true);
    local AllyCreeps = npcBot:GetNearbyCreeps(1600,false);

    local lowest_hp = 100000;
    local weakest_creep = nil;
    for creep_k,creep in pairs(EnemyCreeps)
    do 
        --npcBot:GetEstimatedDamageToTarget
        local creep_name = creep:GetUnitName();
        DotaBotUtility:UpdateCreepHealth(creep);
        --print(creep_name);
        if(creep:IsAlive()) then
            local creep_hp = creep:GetHealth();
            if(lowest_hp > creep_hp) then
                 lowest_hp = creep_hp;
                 weakest_creep = creep;
            end
        end
    end

    if(weakest_creep ~= nil and weakest_creep:GetHealth() / weakest_creep:GetMaxHealth() < 0.5) then
        -- if creep's hp is lower than 70(because I don't Know how much is my damadge!!), try to last hit it.
        --if(DotaBotUtility.NilOrDead(npcBot:GetAttackTarget()) and 
        if(lowest_hp < weakest_creep:GetActualIncomingDamage(
        npcBot:GetAttackDamage(),DAMAGE_TYPE_PHYSICAL)
        + DotaBotUtility:GetCreepHealthDeltaPerSec(weakest_creep) 
        * (npcBot:GetAttackPoint() / npcBot:GetAttackSpeed() + GetUnitToUnitDistance(npcBot,weakest_creep) / 1200)) then
            if(npcBot:GetAttackTarget() == nil) then --StateMachine["attcking creep"]
                npcBot:Action_AttackUnit(weakest_creep,false);
                return;
            elseif(weakest_creep ~= StateMachine["attcking creep"]) then
                StateMachine["attcking creep"] = weakest_creep;
                npcBot:Action_AttackUnit(weakest_creep,true);
                return;
            end
        else
            -- simulation of human attack and stop
            if(npcBot:GetCurrentActionType() == BOT_ACTION_TYPE_ATTACK) then
                npcBot:Action_ClearActions(true);
                return;
            else
                npcBot:Action_AttackUnit(weakest_creep,false);
                return;
            end
        end
        weakest_creep = nil;
        
    end

    for creep_k,creep in pairs(AllyCreeps)
    do 
        --npcBot:GetEstimatedDamageToTarget
        local creep_name = creep:GetUnitName();
        DotaBotUtility:UpdateCreepHealth(creep);
        --print(creep_name);
        if(creep:IsAlive()) then
             local creep_hp = creep:GetHealth();
             if(lowest_hp > creep_hp) then
                 lowest_hp = creep_hp;
                 weakest_creep = creep;
             end
         end
    end

    if(weakest_creep ~= nil) then
        -- if creep's hp is lower than 70(because I don't Know how much is my damadge!!), try to last hit it.
        if(DotaBotUtility.NilOrDead(npcBot:GetAttackTarget()) and 
        lowest_hp < weakest_creep:GetActualIncomingDamage(
        npcBot:GetAttackDamage(),DAMAGE_TYPE_PHYSICAL) + DotaBotUtility:GetCreepHealthDeltaPerSec(weakest_creep) 
        * (npcBot:GetAttackPoint() / npcBot:GetAttackSpeed() + GetUnitToUnitDistance(npcBot,weakest_creep) / 1200)
         and 
        weakest_creep:GetHealth() / weakest_creep:GetMaxHealth() < 0.5) then
            Attacking_creep = weakest_creep;
            npcBot:Action_AttackUnit(Attacking_creep,true);
            return;
        end
        weakest_creep = nil;
        
    end

    -- hit creeps to push
    local TimeNow = DotaTime();
    for creep_k,creep in pairs(EnemyCreeps)
    do 
        local creep_name = creep:GetUnitName();
        --print(creep_name);
        if(creep:IsAlive()) then
            if(TimeNow > 600) then
                npcBot:Action_AttackUnit(creep,false);
                return;
            end
            local creep_hp = creep:GetHealth();
            if(lowest_hp > creep_hp) then
                 lowest_hp = creep_hp;
                 weakest_creep = creep;
            end
        end
    end
    
end

local function IsBusy()
    local npcBot = GetBot();

    local busy = npcBot:IsUsingAbility() or npcBot:IsChanneling() or npcBot:GetCurrentActionType() == BOT_ACTION_TYPE_USE_ABILITY;

    return busy;
end

local function StateIdle(StateMachine)
    local npcBot = GetBot();
    if(npcBot:IsAlive() == false) then
        return;
    end

    local creeps = npcBot:GetNearbyCreeps(1600,true);
    local pt = DotaBotUtility:GetComfortPoint(creeps,LANE);

    if (IsBusy()) then return end;


    if(IsTowerAttackingMe() or DotaBotUtility:ConsiderRunAway()) then
        StateMachine.State = STATE_RUN_AWAY;
        return;
    elseif(#creeps > 0 and pt ~= nil) then
        local mypos = npcBot:GetLocation();
        
        local d = GetUnitToLocationDistance(npcBot,pt);
        if(d > 250) then
            StateMachine.State = STATE_GOTO_COMFORT_POINT;
        else
            StateMachine.State = STATE_ATTACKING_CREEP;
        end
        return;
    end
    
    local NearbyTowers = npcBot:GetNearbyTowers(1600,true);
    local AllyCreeps = npcBot:GetNearbyCreeps(1600,false);

    for _,tower in pairs(NearbyTowers)
    do
        local myDistanceToTower = GetUnitToUnitDistance(npcBot,tower);
        if(tower:IsAlive() and #AllyCreeps >= 1 and #creeps == 0) then
            for _,creep in pairs(AllyCreeps)
            do
                if(myDistanceToTower > GetUnitToUnitDistance(creep,tower) + 300) then
                    --print("SF attack tower!!!");
                    npcBot:Action_AttackUnit(tower,false);
                    return;
                end
            end
        end
    end

    local allycreeps = npcBot:GetNearbyCreeps(1600,false);
    local allypt = DotaBotUtility:GetComfortPoint(allycreeps,LANE);

    if(#allycreeps > 0 and allypt ~= nil) then
        npcBot:Action_MoveToLocation(allypt);
        return;
    else
        local tower = DotaBotUtility:GetFrontTowerAt(LANE);
        npcBot:Action_MoveToLocation(tower:GetLocation());
        return;
    end
    

end

local function StateAttackingCreep(StateMachine)
    local npcBot = GetBot();
    if(npcBot:IsAlive() == false) then
        StateMachine.State = STATE_IDLE;
        return;
    end

    local creeps = npcBot:GetNearbyCreeps(1600,true);
    local pt = DotaBotUtility:GetComfortPoint(creeps,LANE);

    if (IsBusy()) then return end;


    if(IsTowerAttackingMe() or DotaBotUtility:ConsiderRunAway()) then
        StateMachine.State = STATE_RUN_AWAY;
    elseif(#creeps > 0 and pt ~= nil) then
        local mypos = npcBot:GetLocation();
        local d = GetUnitToLocationDistance(npcBot,pt);
        if(d > 200) then
            if(StateMachine["GotoComfortPointTime"] == nil) then
                StateMachine["GotoComfortPointTime"] = GameTime();
                return;
            else
                if(GameTime() - StateMachine["GotoComfortPointTime"] < 0.5) then
                    return;
                else
                    StateMachine.State = STATE_GOTO_COMFORT_POINT;
                    StateMachine["GotoComfortPointTime"] = nil;
                    return;
                end
            end
            
        else
            ConsiderAttackCreeps(StateMachine);
        end
        return;
    else
        StateMachine.State = STATE_IDLE;
        return;
    end
end

local function StateGotoComfortPoint(StateMachine)
    local npcBot = GetBot();
    if(npcBot:IsAlive() == false) then
        StateMachine.State = STATE_IDLE;
        return;
    end

    local creeps = npcBot:GetNearbyCreeps(1600,true);
    local pt = DotaBotUtility:GetComfortPoint(creeps,LANE);
    
    if (IsBusy()) then return end;

    if(IsTowerAttackingMe() or DotaBotUtility:ConsiderRunAway()) then
        StateMachine.State = STATE_RUN_AWAY;
        return;
    elseif(#creeps > 0 and pt ~= nil) then
        local mypos = npcBot:GetLocation();
        --pt[3] = npcBot:GetLocation()[3];
        
        --local d = GetUnitToLocationDistance(npcBot,pt);
        local d = (npcBot:GetLocation() - pt):Length2D();
 
        if (d < 100) then
            StateMachine.State = STATE_ATTACKING_CREEP;
        else
            npcBot:Action_MoveToLocation(pt);
        end
        return;
    else
        StateMachine.State = STATE_IDLE;
        return;
    end

end

local function StateRunAway(StateMachine)
    local npcBot = GetBot();

    if (IsBusy()) then return end;

    if(npcBot:IsAlive() == false) then
        StateMachine.State = STATE_IDLE;
        StateMachine["RunAwayFromLocation"] = nil;
        return;
    end
    local mypos = npcBot:GetLocation();

    if(StateMachine["RunAwayFromLocation"] == nil) then
        --set the target to go back
        StateMachine["RunAwayFromLocation"] = npcBot:GetLocation();
        --npcBot:Action_MoveToLocation(Constant.HomePosition());
        npcBot:Action_MoveToLocation(DotaBotUtility:GetNearByPrecursorPointOnLane(LANE));
        return;
    else
        if(GetUnitToLocationDistance(npcBot,StateMachine["RunAwayFromLocation"]) > 400) then
            -- we are far enough from tower,return to normal state.
            StateMachine["RunAwayFromLocation"] = nil;
            StateMachine.State = STATE_IDLE;
            return;
        else
            npcBot:Action_MoveToLocation(DotaBotUtility:GetNearByPrecursorPointOnLane(LANE));
            return;
        end
    end
end

local StateMachine = {};
StateMachine["State"] = STATE_IDLE;
StateMachine[STATE_IDLE] = StateIdle;
StateMachine[STATE_ATTACKING_CREEP] = StateAttackingCreep;
StateMachine[STATE_GOTO_COMFORT_POINT] = StateGotoComfortPoint;
StateMachine[STATE_RUN_AWAY] = StateRunAway;

function Think(  )
    StateMachine[StateMachine.State](StateMachine);
end