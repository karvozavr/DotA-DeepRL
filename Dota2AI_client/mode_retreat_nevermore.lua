local Constant = require(GetScriptDirectory().."/dev/constant_each_side");

if (true) then

math.randomseed(RealTime())

_G.RetreatDesire = math.random()

function GetDesire()
    return _G.RetreatDesire
end

end

function OnStart()
    _G.state = "retreat"
end

function Think(  )
    local npcBot = GetBot();
    npcBot:Action_MoveToLocation(Constant.HomePosition())
end