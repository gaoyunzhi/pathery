from find_path import find_path
from get_weighted_choice import get_weighted_choice
from get_weighted_random import get_weighted_random
from get_solution_hash import get_solution_hash
from clean_up_solution_space import clean_up_solution_space
from time import time
U = "2"

INIT_ROUND = 100
FOLLOW_UP_ROUND = 10
PULL_UP_TIME = 5

def apply_solution(test_map, solution):
	result_map = [list(line) for line in test_map]
	for i, j in solution:
		result_map[i][j] = U
	return result_map

def find_raw_solution(test_map, solution, N):
	solution = set(solution)
	path_map, dis = find_path(apply_solution(test_map, solution))
	blocking_points = set() 
	M = N - len(solution)
	for _ in xrange(M):
		solution, dis, path_map = pull_up_solution(test_map, solution, blocking_points, path_map)
	return solution, dis

def pull_up_solution(test_map, solution, blocking_points, path_map):
	solution = set(solution)
	weighted_choice = get_weighted_choice(path_map)
	while True:
		point = get_weighted_random(weighted_choice)
		if point in blocking_points:
			continue
		solution.add(point)
		current_map = apply_solution(test_map)
		path_map, dis = find_path(test_map)
		if dis != -1:
			break
		blocking_points.add(point)
		solution.remove(point)
	return solution, dis, path_map

def pull_up_solution_space(solution_space, N):
	for num in solution_space:
		if num == N - 1:
			continue
		for dis in solution_space[num]:
			for solution_key in solution_space[num][dis]:
				solution = solution_space[num][dis][solution_key]
				blocking_points = set()
				path_map, _ = find_path(apply_solution(test_map, solution))
				for x in xrange(PULL_UP_TIME):
					new_solution, dis, _ = pull_up_solution(test_map, solution, blocking_points, path_map)
					add_solution(solution_space, new_solution, dis, num + 1)

def pull_down_solution_space(solution_space):
	for num in solution_space:
		if num <= 1:
			continue
		for dis in solution_space[num]:
			for solution_key in solution_space[num][dis]:
				solution = solution_space[num][dis][solution_key]
				for point in solution:
					new_solution = set(solution)
					new_solution.remove(point)
					_, dis = find_path(apply_solution(test_map, new_solution))
					add_solution(solution_space, new_solution, dis, num - 1)

def add_solution(solution_space, solution, dis, num):
	solution_space[num][dis] = solution_space[num].get(dis, {})
	solution_space[num][dis][get_solution_hash(solution)] = solution

def find_solution(test_map, N):
	solution_space = {}
	for i in xrange(N + 1):
		solution_space[i] = {}
	start_time = time()
	for _ in xrange(INIT_ROUND):
		solution, dis = find_raw_solution(test_map, set(), N)
		add_solution(solution_space, solution, dis)
	print "INIT ROUND", int((time() - start_time))
	clean_up_solution_space(solution_space)
	while _ in xrange(FOLLOW_UP_ROUND):
		start_time = time()
		pull_down_solution_space(solution_space)
		print "PULL_DOWN", int((time() - start_time))
		clean_up_solution_space(solution_space)
		start_time = time()
		pull_up_solution_space(solution_space, N)
		print "PULL_UP", int((time() - start_time))
		clean_up_solution_space(solution_space)
	dis = max(solution_space[N].keys())
	solution = solution_space[N][dis].itervalues().next()
	solution_map = apply_solution(test_map, solution)
	return solution_map, solution, dis
