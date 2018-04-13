require(GetScriptDirectory()..'/util/json')

local Observation = require(GetScriptDirectory() .. '/agent_utils/observation')
local Reward = require(GetScriptDirectory() .. '/agent_utils/reward')
local Action = require(GetScriptDirectory() .. '/agent_utils/action')

local action_ready = false
local state_num = 0

-- On action recieved callback.
function action_recieved(action)
    print('action_recieved event')

    current_action = action
    action_ready = true
end

-- Send JSON with current state info.
-- @param message JSON state info
function send_state_message(message)
    local req = CreateHTTPRequest(':5000')
    req:SetHTTPRequestRawPostBody('application/json', message)
    print('send')
    req:Send( 
        function(result)
            for k, v in pairs(result) do
                if k == 'Body' then
                    print(string.format( "%s : %s\n", k, v ))
                    if v ~= '' then 
                        action_recieved(Json.Decode(v))
                    end
                end 
            end
        end
    )
end

function send_game_state()
    local _end = 0

    if GetGameState() == GAME_STATE_POST_GAME then
        _end = 1
        print('Bot: the game has ended.')
    end

    msg = {
        ['observation'] = Observation.get_observation(),
        ['reward'] = Reward.get_reward(),
        ['done'] = _end,
        ['state_num'] = state_num
    }

    encode_msg = Json.Encode(msg)
    send_state_message(encode_msg)

    state_num = state_num + 1
end

-- Execute action.
function execute_action(action)
    print("Execute action.", action)
    Action.move_delta(action)
    action_ready = false
end

local last_time_sent = GameTime()

function Think()
    local _time = DotaTime()
    if (GetGameState() == GAME_STATE_GAME_IN_PROGRESS or GetGameState() == GAME_STATE_PRE_GAME or GetGameState() == GAME_STATE_POST_GAME) then
        if action_ready == true then
            execute_action(current_action)
        elseif GameTime() - last_time_sent > 0.1 then
            send_game_state()
            last_time_sent = GameTime()
        end
    end
end