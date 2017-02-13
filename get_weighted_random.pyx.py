from random import choice
from get_solution_hash import get_solution_hash

def get_weighted_random(next_points, probability_space, solution, computed_solutions, accompany_space, do_random):
	contangent_points, recommended_points = next_points
	if not contangent_points:
		return []
	n = len(probability_space) * 1.0

	solution = set(solution)
	to_discard = set()
	for p in contangent_points:
		solution.add(p)
		solution_hash = get_solution_hash(solution)
		if solution_hash in computed_solutions:
			to_discard.add(solution_hash)
	for p in to_discard:
		contangent_points.discard(p)
		recommended_points.discard(p)

	bust_score = n * 0.1
	range_map = {}
	scores = []
	start = 0.0
	for x, y in contangent_points:
		weight = probability_space[x][y]
		if (x, y) in recommended_points:
			weight += bust_score
		range_map[(x, y)] = (start, start + weight)
		scores.append((weight, (x, y)))
		start += weight
	scores.sort(reverse=True)
	result_list = []
	# result = set([s[1] for s in scores if s[0] > n * 0.3])
	# result_list = list(result)
	result = set([])
	leftover = [s[1] for s in scores[len(result):]]
	if leftover and do_random:
		c = choice(leftover)
		result.add(c)
		result_list = [c] + result_list

	for p in solution:
		for p1 in accompany_space.get(p, []):
			if not p1 in solution and not p1 in result:
				result_list.append(p1)
	return result_list
