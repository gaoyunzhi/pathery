def get_solution_hash(solution):
	s = list(solution)
	s.sort()
	return tuple(s)