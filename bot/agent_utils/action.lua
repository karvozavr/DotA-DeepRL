Action = {}

local bot = GetBot()

function Action.move_delta(delta_vector)
	local position = bot:GetLocation()

	position[1] = position[1] + delta_vector[1]
	position[2] = position[2] + delta_vector[2]

	bot:Action_MoveDirectly(position)
end

return Action;