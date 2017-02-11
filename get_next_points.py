from apply_solution import apply_solution
from get_solution_hash import get_solution_hash
from in_boundary import in_boundary
O = "0"

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
LOOP = {(-1, -1): 0, (-1, 0): 1, (-1, 1): 2, (0, 1): 3, (1, 1): 4, (1, 0): 5, (1, -1): 6, (0, -1): 7}

def _get_next_points(test_map):
	L = len(test_map)
	W = len(test_map[0])
	contangent_points = set()
	recommended_points = set()
	for x in xrange(L):
		for y in xrange(W):
			if not test_map[x][y] == O:
				continue
			loop = [0] * 8
			for dx in xrange(-1, 2):
				for dy in xrange(-1, 2):
					nx, ny = x + dx, y + dy
					if not in_boundary(nx, ny, L, W) or test_map[nx][ny] != O:
						contangent_points.add((x, y))	
						loop[LOOP[(dx, dy)]] = 1
			white_length = 0
			i = 0
			while i < 8 and loop[i] == 0:
				white_length += 1
				i += 1
			i = 7
			while i >= 0 and loop[i] == 0:
				white_length += 1
				i -= 1
			if white_length < 8 - sum(loop):
				recommended_points.add((x, y))
	return (contangent_points, recommended_points)

def get_next_points(cache_next_points, solution, test_map):
	solution_hash = get_solution_hash(solution)
	if solution_hash in cache_next_points:
		return cache_next_points[solution_hash]
	test_map_new = apply_solution(test_map, solution)
	next_points = _get_next_points(test_map_new)
	cache_next_points[solution_hash] = next_points
	return next_points
