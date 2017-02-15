from find_dis import find_dis
from get_solution_hash import get_solution_hash
from get_printable_map import get_printable_map
from time import clock
from get_weighted_random import get_weighted_random
from get_solution_distribution import get_solution_distribution
from get_next_points import get_next_points
from random import sample
from apply_solution import apply_solution
from convert_accompany_space import convert_accompany_space
from solution_space import SolutionSpace
from populated_structure_solutions import populated_structure_solutions

RAW_ROUND = 500
NUM_ROUND = 1000
PULL_UP_TIME = 1
SAMPLE_LIMIT_DELTA = 2
CEILING_HIGH = 3

def add_raw_solution(test_map, N, solution_space, computed_solutions, num_round, probability_space, cache_next_points, accompany_space):
	solution = set()
	for n in xrange(1, N + CEILING_HIGH):
		new_solution = None
		for _ in xrange(10):
			new_solution = pull_up_solution(test_map, solution, solution_space, computed_solutions, num_round, probability_space, cache_next_points, accompany_space, True)
			if new_solution != None:
				break
		if new_solution == None:
			return
		solution = new_solution

def pull_up_solution(test_map, solution, solution_space, computed_solutions, num_round, probability_space, cache_next_points, accompany_space, do_random):
	solution = set(solution)
	next_points = get_next_points(cache_next_points, solution, test_map)
	points = get_weighted_random(next_points, probability_space, solution, computed_solutions, accompany_space, do_random)
	last_good_solution = None
	for point in points:
		solution.add(point)
		dis = find_dis(apply_solution(test_map, solution))
		if dis == -1:
			computed_solutions[get_solution_hash(solution)] = -1
		else:
			add_solution(solution_space, solution, dis, computed_solutions, num_round)	
			last_good_solution = set(solution)
		next_points[0].discard(point)
		next_points[1].discard(point)
		solution.remove(point)
	return last_good_solution

def pull_up_solution_space(solution_space, test_map, N, computed_solutions, num_round, probability_space, cache_next_points, accompany_space):
	for num in sorted(solution_space.keys()):
		if num >= N + CEILING_HIGH:
			continue
		sample_limit = SAMPLE_LIMIT_DELTA * 5
		count = 0
		for dis in sorted(solution_space[num].keys(), reverse=True)[:4]:
			sample_limit -= SAMPLE_LIMIT_DELTA
			do_random = len(solution_space[num][dis]) < 100
			items = solution_space[num][dis].items() # List of tuples
			new_items = [item for item in items if computed_solutions[item[0]] > num_round - 2]
			if len(new_items) > sample_limit:
				new_items = sample(new_items, sample_limit)
			if len(items) > sample_limit:
				items = sample(items, sample_limit)
			for solution_key, solution in items + new_items:
				pull_up_solution(test_map, solution, solution_space, computed_solutions, num_round, probability_space, cache_next_points, accompany_space, do_random)
			count += len(solution_space[num][dis])
			if count > 100:
				break

def pull_down_solution_space(solution_space, test_map, computed_solutions, num_round, probability_space, accompany_space):
	for num in sorted(solution_space.keys())[::-1]:
		if num <= 1:
			continue
		distances = sorted(solution_space[num].keys())[-4:]
		top = 0
		for dis in distances:
			reverse_weight = len(solution_space[num][dis]) + 1
			if top == 0 and reverse_weight < 20:
				for solution_key in solution_space[num][dis]:
					solution = solution_space[num][dis][solution_key]
					add_to_probability_space(probability_space, solution, reverse_weight)
					add_to_accompany_space(solution, accompany_space, reverse_weight)

			count = 0
			module = reverse_weight / (100 / (2 ** top)) + 1
			for solution_key in solution_space[num][dis]:	
				count += 1
				if count % module != 0 or computed_solutions[solution_key] < num_round - 1:
					continue 
				solution = solution_space[num][dis][solution_key]
				new_solution = set(solution)
				for point in solution:
					new_solution.remove(point)
					if not get_solution_hash(new_solution) in computed_solutions:
						new_dis = find_dis(apply_solution(test_map, new_solution))
						add_solution(solution_space, new_solution, new_dis, computed_solutions, num_round)
					new_solution.add(point)
			top += 1

def add_to_probability_space(probability_space, solution, reverse_weight):
	for x, y in solution:
		probability_space[x][y] += 1.0 / reverse_weight / reverse_weight

def add_to_accompany_space(solution, accompany_space, reverse_weight):
	for x, y in solution:
		if not (x, y) in accompany_space:
			accompany_space[(x, y)] = {}
		for x1, y1 in solution:
			if x == x1 and y == y1:
				continue
			if not (x1, y1) in accompany_space[(x, y)]:
				accompany_space[(x, y)][(x1, y1)] = 0
			accompany_space[(x, y)][(x1, y1)] += 1.0 / reverse_weight / reverse_weight

def add_solution(solution_space, solution, dis, computed_solutions, num_round):
	num = len(solution)
	solution_space[num][dis] = solution_space[num].get(dis, {})
	solution_space[num][dis][get_solution_hash(solution)] = set(solution)
	computed_solutions[get_solution_hash(solution)] = num_round

def get_init_probability_space(test_map):
	return [[0.1 for _ in line] for line in test_map]

def find_solution(test_map, N, ANS):
	LEVEL = 0
	solution_space = SolutionSpace(test_map, N, ANS)
	solution_space.add(set())
	populated_structure_solutions(solution_space, test_map, N)
	


		

	# 		solution_map = apply_solution(test_map, solution)
	# 		print "RAW_ROUND", raw_round
	# 		print "PULL_DOWN", pull_down
	# 		print "PULL_UP", pull_up
	# 		print get_printable_map(solution_map)
	# 		print get_solution_distribution(solution_space), 
	# 		print num_round, dis
	# dis = max(solution_space[N].keys())
	# solution = solution_space[N][dis].itervalues().next()
	# solution_map = apply_solution(test_map, solution)
	# return N, get_printable_map(solution_map), solution, dis
