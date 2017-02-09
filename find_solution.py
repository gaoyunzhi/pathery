from find_path import find_path
from get_weighted_choice import get_weighted_choice
from get_weighted_random import get_weighted_random
from get_solution_hash import get_solution_hash
from clean_up_solution_space import clean_up_solution_space
from get_printable_map import get_printable_map
from time import time
U = "2"

INIT_ROUND = 100
FOLLOW_UP_ROUND = 100
PULL_UP_TIME = 5

def apply_solution(test_map, solution):
	result_map = [list(line) for line in test_map]
	for i, j in solution:
		result_map[i][j] = U
	return result_map

def add_raw_solution(test_map, N, solution_space, computed_solutions):
	path_map, dis = find_path(test_map)
	solution = set()
	for n in xrange(1, N + 1):
		solution, dis, path_map = pull_up_solution(test_map, solution, set(), path_map, computed_solutions)
		if solution == None:
			return
		add_solution(solution_space, solution, dis, n)

def pull_up_solution(test_map, solution, blocking_points, path_map, computed_solutions):
	solution = set(solution)
	weighted_choice = get_weighted_choice(path_map)
	while True:
		point = get_weighted_random(weighted_choice, blocking_points)
		if point == None:
			return None, None, None
		solution.add(point)
		if get_solution_hash(solution) in computed_solutions:
			blocking_points.add(point)
			continue
		computed_solutions.add(get_solution_hash(solution))
		path_map, dis = find_path(apply_solution(test_map, solution))
		if dis != -1:
			break
		blocking_points.add(point)
		solution.remove(point)
	return solution, dis, path_map

def pull_up_solution_space(solution_space, test_map, N, computed_solutions):
	for num in solution_space:
		if num == N or num < N - 2:
			continue
		for dis in solution_space[num]:
			for solution_key in solution_space[num][dis]:
				solution = solution_space[num][dis][solution_key]
				blocking_points = set()
				path_map, _ = find_path(apply_solution(test_map, solution))
				for x in xrange(PULL_UP_TIME):
					new_solution, new_dis, _ = pull_up_solution(test_map, solution, blocking_points, path_map, computed_solutions)
					if new_solution == None:
						break
					add_solution(solution_space, new_solution, new_dis, num + 1)

def pull_down_solution_space(solution_space, test_map, computed_solutions):
	for num in solution_space:
		if num <= 1:
			continue
		for dis in solution_space[num]:
			for solution_key in solution_space[num][dis]:
				solution = solution_space[num][dis][solution_key]
				for point in solution:
					new_solution = set(solution)
					new_solution.remove(point)
					if get_solution_hash(solution) in computed_solutions:
						continue
					computed_solutions.add(get_solution_hash(solution))
					_, new_dis = find_path(apply_solution(test_map, new_solution))
					add_solution(solution_space, new_solution, new_dis, num - 1)

def add_solution(solution_space, solution, dis, num):
	solution_space[num][dis] = solution_space[num].get(dis, {})
	solution_space[num][dis][get_solution_hash(solution)] = solution

def find_solution(test_map, N):
	solution_space = {}
	for i in xrange(N + 1):
		solution_space[i] = {}
	start_time = time()
	computed_solutions = set()
	for _ in xrange(INIT_ROUND):
		add_raw_solution(test_map, N, solution_space, computed_solutions)
	print "INIT ROUND", int((time() - start_time) * 1000)
	clean_up_solution_space(solution_space)
	for _ in xrange(FOLLOW_UP_ROUND):
		start_time = time()
		pull_down_solution_space(solution_space, test_map, computed_solutions)
		print "PULL_DOWN", int((time() - start_time) * 1000)
		clean_up_solution_space(solution_space)
		start_time = time()
		pull_up_solution_space(solution_space, test_map, N, computed_solutions)
		print "PULL_UP", int((time() - start_time) * 1000)
		clean_up_solution_space(solution_space)
		## test
		dis = max(solution_space[N].keys())
		solution = solution_space[N][dis].itervalues().next()
		solution_map = apply_solution(test_map, solution)
		print _, get_printable_map(solution_map), solution, dis
	dis = max(solution_space[N].keys())
	solution = solution_space[N][dis].itervalues().next()
	solution_map = apply_solution(test_map, solution)
	return N, get_printable_map(solution_map), solution, dis
