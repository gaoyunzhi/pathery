from find_path import find_path
from get_solution_hash import get_solution_hash
from clean_up_solution_space import clean_up_solution_space
from get_printable_map import get_printable_map
from time import clock
from random import sample
U = "2"

RAW_ROUND = 15
NUM_ROUND = 1000
PULL_UP_TIME = 1
SAMPLE_LIMIT_DELTA = 2

def apply_solution(test_map, solution):
	result_map = [list(line) for line in test_map]
	for i, j in solution:
		result_map[i][j] = U
	return result_map

def add_raw_solution(test_map, N, solution_space, computed_solutions, num_round):
	path_map, dis = find_path(test_map)
	solution = set()
	for n in xrange(1, N + 4):
		solution, dis, path_map = pull_up_solution(test_map, solution, set(), path_map, solution_space, computed_solutions, num_round)
		if solution == None:
			return

def pull_up_solution(test_map, solution, blocking_points, path_map, solution_space, computed_solutions, num_round):
	solution = set(solution)
	while True:
		choice = path_map - blocking_points
		if not choice:
			return None, None, None
		point = sample(choice, 1)[0]
		solution.add(point)
		if get_solution_hash(solution) in computed_solutions:
			blocking_points.add(point)
			solution.remove(point)
			continue
		apply_solution(test_map, solution)
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
		if num > N + 2:
			continue
		sample_limit = 0
		for dis in sorted(solution_space[num].keys())[-4:]:
			sample_limit += SAMPLE_LIMIT_DELTA
			items=solution_space[num][dis].items() # List of tuples
			new_items = [item for item in items if computed_solutions[item[0]] == num_round]
			if len(new_items) > sample_limit:
				new_items = sample(new_items, sample_limit)
			if len(items) > sample_limit:
				items = sample(items, sample_limit)
			for solution_key, solution in items + new_items:
				blocking_points = set()
				path_map, _ = find_path(apply_solution(test_map, solution))
				for x in xrange(PULL_UP_TIME * sample_limit * 2 / len(items + new_items)):
					new_solution, new_dis, _ = \
						pull_up_solution(test_map, solution, blocking_points, path_map, solution_space, computed_solutions, num_round)
					if new_solution == None:
						break

def pull_down_solution_space(solution_space, test_map, computed_solutions, num_round):
	for num in solution_space:
		if num <= 1:
			continue
		distances = sorted(solution_space[num].keys())[-2:]
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
	for i in xrange(N + 10):
		solution_space[i] = {}
	start_time = clock()
	computed_solutions = {}
	for _ in xrange(RAW_ROUND):
		add_raw_solution(test_map, N, solution_space, computed_solutions, 0)
	for num_round in xrange(1, NUM_ROUND):
		start_time = clock()
		for _ in xrange(RAW_ROUND):
			add_raw_solution(test_map, N, solution_space, computed_solutions, num_round)
		clean_up_solution_space(solution_space)
		raw_round = int((clock() - start_time) * 1000)
		start_time = clock()
		pull_down_solution_space(solution_space, test_map, computed_solutions, num_round)
		clean_up_solution_space(solution_space)
		pull_down = int((clock() - start_time) * 1000)
		start_time = clock()
		pull_up_solution_space(solution_space, test_map, N, computed_solutions, num_round)
		clean_up_solution_space(solution_space)
		pull_up = int((clock() - start_time) * 1000)
		## test
		if num_round % 10 == 0:
			dis = max(solution_space[N].keys())
			solution = solution_space[N][dis].itervalues().next()
			solution_map = apply_solution(test_map, solution)
			print "RAW_ROUND", raw_round
			print "PULL_DOWN", pull_down
			print "PULL_UP", pull_up
			print get_printable_map(solution_map), len(solution_space[N][dis]), solution, num_round, dis
	dis = max(solution_space[N].keys())
	solution = solution_space[N][dis].itervalues().next()
	solution_map = apply_solution(test_map, solution)
	return N, get_printable_map(solution_map), solution, dis
