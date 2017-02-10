from find_path import find_path
from get_weighted_choice import get_weighted_choice
from get_weighted_random import get_weighted_random
from get_solution_hash import get_solution_hash
from clean_up_solution_space import clean_up_solution_space
from get_printable_map import get_printable_map
from time import time
from random import sample
U = "2"

RAW_ROUND = 100
NUM_ROUND = 500
PULL_UP_TIME = 2
SAMPLE_LIMIT = 10

def apply_solution(test_map, solution):
	result_map = [list(line) for line in test_map]
	for i, j in solution:
		result_map[i][j] = U
	return result_map

def add_raw_solution(test_map, N, solution_space, computed_solutions, num_round):
	path_map, dis = find_path(test_map)
	solution = set()
	for n in xrange(1, N + 1):
		solution, dis, path_map = pull_up_solution(test_map, solution, set(), path_map, solution_space, computed_solutions, num_round)
		if solution == None:
			return

def pull_up_solution(test_map, solution, blocking_points, path_map, solution_space, computed_solutions, num_round):
	solution = set(solution)
	weighted_choice = get_weighted_choice(path_map)
	while True:
		point = get_weighted_random(weighted_choice, blocking_points)
		if point == None:
			return None, None, None
		solution.add(point)
		if get_solution_hash(solution) in computed_solutions:
			blocking_points.add(point)
			solution.remove(point)
			continue
		path_map, dis = find_path(apply_solution(test_map, solution))
		if dis != -1:
			computed_solutions[get_solution_hash(solution)] = -1
			break
		blocking_points.add(point)
		solution.remove(point)
	add_solution(solution_space, solution, dis, len(solution), computed_solutions, num_round)
	return solution, dis, path_map

def pull_up_solution_space(solution_space, test_map, N, computed_solutions, num_round):
	for num in sorted(solution_space.keys()):
		if num == N:
			continue
		for dis in sorted(solution_space[num].keys()):
			items=solution_space[num][dis].items() # List of tuples
			if len(items) > SAMPLE_LIMIT:
				items = sample(items, SAMPLE_LIMIT)
				items = [item for item in items if computed_solutions[item[0]] == num_round] + \
					 sample(items, SAMPLE_LIMIT)
			for solution_key, solution in items:
				blocking_points = set()
				path_map, _ = find_path(apply_solution(test_map, solution))
				for x in xrange(PULL_UP_TIME):
					new_solution, new_dis, _ = \
						pull_up_solution(test_map, solution, blocking_points, path_map, solution_space, computed_solutions, num_round)
					if new_solution == None:
						break

def pull_down_solution_space(solution_space, test_map, computed_solutions, num_round):
	for num in solution_space:
		if num <= 1:
			continue
		distances = sorted(solution_space[num].keys())[-4:]
		for dis in distances:
			for solution_key in solution_space[num][dis]:
				solution = solution_space[num][dis][solution_key]
				for point in solution:
					new_solution = set(solution)
					new_solution.remove(point)
					if get_solution_hash(solution) in computed_solutions:
						continue
					_, new_dis = find_path(apply_solution(test_map, new_solution))
					add_solution(solution_space, new_solution, new_dis, num - 1, computed_solutions, num_round)

def add_solution(solution_space, solution, dis, num, computed_solutions, num_round):
	solution_space[num][dis] = solution_space[num].get(dis, {})
	solution_space[num][dis][get_solution_hash(solution)] = solution
	computed_solutions[get_solution_hash(solution)] = num_round

def find_solution(test_map, N):
	solution_space = {}
	for i in xrange(N + 1):
		solution_space[i] = {}
	start_time = time()
	computed_solutions = {}
	for num_round in xrange(NUM_ROUND):
		start_time = time()
		for _ in xrange(RAW_ROUND):
			add_raw_solution(test_map, N, solution_space, computed_solutions, num_round)
		clean_up_solution_space(solution_space)
		print "RAW_ROUND", int((time() - start_time) * 1000)
		start_time = time()
		pull_down_solution_space(solution_space, test_map, computed_solutions, num_round)
		clean_up_solution_space(solution_space)
		print "PULL_DOWN", int((time() - start_time) * 1000)
		start_time = time()
		pull_up_solution_space(solution_space, test_map, N, computed_solutions, num_round)
		clean_up_solution_space(solution_space)
		print "PULL_UP", int((time() - start_time) * 1000)
		## test
		if num_round % 10 == 0:
			dis = max(solution_space[N].keys())
			solution = solution_space[N][dis].itervalues().next()
			solution_map = apply_solution(test_map, solution)
			print get_printable_map(solution_map), solution, num_round, dis
	dis = max(solution_space[N].keys())
	solution = solution_space[N][dis].itervalues().next()
	solution_map = apply_solution(test_map, solution)
	return N, get_printable_map(solution_map), solution, dis
