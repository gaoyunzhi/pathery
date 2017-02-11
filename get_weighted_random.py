from random import choice
from get_solution_hash import get_solution_hash

def get_weighted_random(next_points, probability_space, solution, computed_solutions):
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
	result = [s[1] for s in scores if s[0] > n * 0.3]
	if not result:
		result.append(scores[0][1])
	leftover = [s[1] for s in scores[len(result):]]
	if leftover:
		result.append(choice(leftover))
	return result
