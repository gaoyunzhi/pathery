U = "2"

def apply_solution(test_map, solution):
	result_map = [list(line) for line in test_map]
	for i, j in solution:
		result_map[i][j] = U
	return result_map