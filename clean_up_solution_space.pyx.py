LIMIT = 20
LEVEL_LIMIT = 100

def clean_up_solution_space(solution_space):
	for current_number in solution_space:
		if len(solution_space[current_number].keys()) == 0:
			continue
		max_dis = max(solution_space[current_number].keys())
		limit = 0
		current_dis = max_dis
		while (limit < LIMIT or current_dis >= max_dis - LEVEL_LIMIT) and current_dis > 0:
			limit += len(solution_space[current_number].get(current_dis, {}).keys())
			current_dis -= 1
		for dis in xrange(current_dis + 1):
			solution_space[current_number].pop(dis, None)