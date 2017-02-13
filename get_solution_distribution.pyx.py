def get_solution_distribution(solution_space):
	res = []
	for num in sorted(solution_space.keys()):
		if not solution_space[num].keys():
			continue
		dis = max(solution_space[num].keys())
		res.append((num, dis, len(solution_space[num][dis])))
	return res