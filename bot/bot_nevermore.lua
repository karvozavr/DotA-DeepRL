require(GetScriptDirectory() .. '/util/json')

local Observation = require(GetScriptDirectory() .. '/agent_utils/observation')
local Reward = require(GetScriptDirectory() .. '/agent_utils/reward')
local Action = require(GetScriptDirectory() .. '/agent_utils/action')

local current_action
local state_num = 0

-- Bot to server comunication FSM.
local WHAT_NEXT = 0
local ACTION_RECEIVED = 1
local SEND_OBSERVATION = 2
local DO_NOTHING = 3
local fsm_state = WHAT_NEXT

-- Execute action.
function execute_action(action)
    print("Execute action.", action)
    Action.move_to_position(GetTower(TEAM_DIRE, TOWER_MID_1):GetLocation())
end

-- Create JSON message from table 'message' of type 'type'
function create_message(message, type)
    local msg = {
        ['type'] = type,
        ['content'] = message
    }

    local encode_msg = Json.Encode(msg)
    return encode_msg
end

-- Send JSON message to bot server.
function send_message(json_message, route, callback)
    local req = CreateHTTPRequest(':5000' .. route)
    req:SetHTTPRequestRawPostBody('application/json', json_message)
    req:Send(function(result)
        for k, v in pairs(result) do
            if k == 'Body' then
                if v ~= '' then
                    local responce = Json.Decode(v)
                    if callback ~= nil then
                        callback(responce)
                    end
                    current_action = responce['action']
                    fsm_state = responce['fsm_state']
                else
                    fsm_state = WHAT_NEXT
                end
            end
        end
    end)
end

-- Ask what to do next.
function send_what_next_message()
    local message = create_message('', 'what_next')
    send_message(message, '/what_next', nil)
end

-- Send JSON with current state info.
function send_observation_message()
    local _end = false

    if GetGameState() == GAME_STATE_POST_GAME then
        _end = true
        print('Bot: the game has ended.')
    end

    local msg = {
        ['observation'] = Observation.get_observation(),
        ['reward'] = Reward.get_reward(),
        ['done'] = _end,
        ['state_num'] = state_num
    }

    send_message(create_message(msg, 'state'), '/observation', nil)
    state_num = state_num + 1
end

local last_time_sent = GameTime()

function Think()
    if (GetGameState() == GAME_STATE_GAME_IN_PROGRESS or GetGameState() == GAME_STATE_PRE_GAME or GetGameState() == GAME_STATE_POST_GAME) then
        if fsm_state == WHAT_NEXT then
            fsm_state = DO_NOTHING
            send_what_next_message()
        elseif fsm_state == SEND_OBSERVATION then
            fsm_state = DO_NOTHING
            send_observation_message()
            last_time_sent = GameTime()
        elseif fsm_state == ACTION_RECEIVED then
            fsm_state = WHAT_NEXT
            execute_action(current_action)
        elseif fsm_state == DO_NOTHING then
            -- Do nothing
        end
    end
end