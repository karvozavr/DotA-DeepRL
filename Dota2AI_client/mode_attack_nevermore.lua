if (true) then

math.randomseed(RealTime())

_G.AttackDesire = math.random()

function GetDesire()
    return _G.AttackDesire
end

end


function OnStart()
    _G.state = "attack"
    local bot = GetBot()
    bot:Action_ClearActions(true)
end

function GetPointAtRange(distance)
    local npcBot = GetBot()
    local facing = npcBot:GetFacing()
    local rad_facing = math.rad(facing)
    local vec = Vector(math.cos(rad_facing) * distance,
    math.sin(rad_facing) * distance)
    return npcBot:GetLocation() + vec
end

function CheckRaze(distance)
    local npcBot = GetBot()
    local enemyBot = GetUnitList(UNIT_LIST_ENEMY_HEROES)[1]
    if enemyBot == nil then
        return false
    end
    local raze_at = GetPointAtRange(distance)
    local d = (raze_at - enemyBot:GetLocation()):Length2D()
    return d <= 125
end

function Think(  )
    local npcBot = GetBot()
    local facing = npcBot:GetFacing()
    local rad_facing = math.rad(facing)

    local enemyBot = GetUnitList(UNIT_LIST_ENEMY_HEROES)[1]

    if(enemyBot ~= nil) then 
        npcBot:SetTarget(enemyBot)
    else
        return
    end

    -- Check if we're already using an ability
	if ( npcBot:IsUsingAbility() ) then return end;

    local raze1 = npcBot:GetAbilityByName("nevermore_shadowraze1")
    if raze1:IsFullyCastable() and CheckRaze(200) then
        npcBot:Action_UseAbility(raze1)
        return
    end

    local raze2 = npcBot:GetAbilityByName("nevermore_shadowraze2")
    if raze2:IsFullyCastable() and CheckRaze(450) then
        npcBot:Action_UseAbility(raze2)
        return
    end

    local raze3 = npcBot:GetAbilityByName("nevermore_shadowraze3")
    if raze3:IsFullyCastable() and CheckRaze(700) then
        npcBot:Action_UseAbility(raze3)
        return
    end

    if GetUnitToUnitDistance(npcBot,enemyBot) < npcBot:GetAttackRange() then
        npcBot:Action_AttackUnit(enemyBot, false)
    else
        npcBot:Action_MoveToUnit(enemyBot)
    end
end