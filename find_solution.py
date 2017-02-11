from find_dis import find_dis
from get_solution_hash import get_solution_hash
from get_printable_map import get_printable_map
from time import clock
from get_weighted_random import get_weighted_random
from get_solution_distribution import get_solution_distribution
from get_next_points import get_next_points
from random import sample
from apply_solution import apply_solution


RAW_ROUND = 50
NUM_ROUND = 1000
PULL_UP_TIME = 1
SAMPLE_LIMIT_DELTA = 2
CEILING_HIGH = 3

def add_raw_solution(test_map, N, solution_space, computed_solutions, num_round, probability_space, cache_next_points):
	solution = set()
	for n in xrange(1, N + CEILING_HIGH):
		solution = pull_up_solution(test_map, solution, solution_space, computed_solutions, num_round, probability_space, cache_next_points)
		if solution == None:
			return

def pull_up_solution(test_map, solution, solution_space, computed_solutions, num_round, probability_space, cache_next_points):
	solution = set(solution)
	next_points = get_next_points(cache_next_points, solution, test_map)
	points = get_weighted_random(next_points, probability_space, solution, computed_solutions)
	last_good_solution = None
	for point in points:
		solution.add(point)
		apply_solution(test_map, solution)
		dis = find_dis(apply_solution(test_map, solution))
		if dis == -1:
			computed_solutions[get_solution_hash(solution)] = -1
		else:
			add_solution(solution_space, solution, dis, computed_solutions, num_round)	
			last_good_solution = solution	
		next_points[0].discard(point)
		next_points[1].discard(point)
		solution.remove(point)
	return last_good_solution

def pull_up_solution_space(solution_space, test_map, N, computed_solutions, num_round, probability_space, cache_next_points):
	for num in sorted(solution_space.keys()):
		if num >= N + CEILING_HIGH:
			continue
		sample_limit = 0
		for dis in sorted(solution_space[num].keys())[-4:]:
			sample_limit += SAMPLE_LIMIT_DELTA
			items=solution_space[num][dis].items() # List of tuples
			new_items = [item for item in items if computed_solutions[item[0]] > num_round - 2]
			if len(new_items) > sample_limit:
				new_items = sample(new_items, sample_limit)
			if len(items) > sample_limit:
				items = sample(items, sample_limit)
			for solution_key, solution in items + new_items:
				pull_up_solution(test_map, solution, solution_space, computed_solutions, num_round, probability_space, cache_next_points)

def pull_down_solution_space(solution_space, test_map, computed_solutions, num_round, probability_space):
	for num in sorted(solution_space.keys())[::-1]:
		if num <= 1:
			continue
		distances = sorted(solution_space[num].keys())[-1:]
		for dis in distances:
			reverse_weight = len(solution_space[num][dis])
			for solution_key in solution_space[num][dis]:
				solution = solution_space[num][dis][solution_key]
				add_to_probability_space(probability_space, solution, reverse_weight)
				if computed_solutions[get_solution_hash(solution)] < num_round - 1:
					continue
				new_solution = set(solution)
				for point in solution:
					new_solution.remove(point)
					if not get_solution_hash(new_solution) in computed_solutions:
						new_dis = find_dis(apply_solution(test_map, new_solution))
						add_solution(solution_space, new_solution, new_dis, computed_solutions, num_round)
					new_solution.add(point)

def add_to_probability_space(probability_space, solution, reverse_weight):
	for x, y in solution:
		probability_space[x][y] += 1.0 / reverse_weight

def add_solution(solution_space, solution, dis, computed_solutions, num_round):
	num = len(solution)
	solution_space[num][dis] = solution_space[num].get(dis, {})
	solution_space[num][dis][get_solution_hash(solution)] = set(solution)
	computed_solutions[get_solution_hash(solution)] = num_round

def get_init_probability_space(test_map):
	return [[0.1 for _ in line] for line in test_map]

def find_solution(test_map, N):
	solution_space = {}
	for i in xrange(N + CEILING_HIGH + 1):
		solution_space[i] = {}
	start_time = clock()
	computed_solutions = {}
	cache_next_points = {}
	probability_space = get_init_probability_space(test_map)
	for num_round in xrange(1, NUM_ROUND):
		start_time = clock()
		for _ in xrange(RAW_ROUND):
			add_raw_solution(test_map, N, solution_space, computed_solutions, num_round, probability_space, cache_next_points)
		probability_space = get_init_probability_space(test_map)
		raw_round = int((clock() - start_time) * 1000)
		start_time = clock()
		pull_down_solution_space(solution_space, test_map, computed_solutions, num_round, probability_space)
		pull_down = int((clock() - start_time) * 1000)
		start_time = clock()
		pull_up_solution_space(solution_space, test_map, N, computed_solutions, num_round, probability_space, cache_next_points)
		pull_up = int((clock() - start_time) * 1000)
		## test
		if num_round % 10 == 0:
			dis = max(solution_space[N].keys())
			solution = solution_space[N][dis].itervalues().next()
			solution_map = apply_solution(test_map, solution)
			print "RAW_ROUND", raw_round
			print "PULL_DOWN", pull_down
			print "PULL_UP", pull_up
			print get_printable_map(solution_map)
			print get_solution_distribution(solution_space), 
			print num_round, dis
	dis = max(solution_space[N].keys())
	solution = solution_space[N][dis].itervalues().next()
	solution_map = apply_solution(test_map, solution)
	return N, get_printable_map(solution_map), solution, dis
