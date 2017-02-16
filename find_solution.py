from time import clock
from solution_space import SolutionSpace
from populated_structure_solutions import populated_structure_solutions
from solution_puller import SolutionPuller
from next_point import NextPoint
from dis_finder import DisFinder

def find_solution(test_map, N, ANS):
	time0 = clock()
	dis_finder = DisFinder(test_map)
	solution_space = SolutionSpace(test_map, N, ANS, dis_finder)
	solution_space.add(set())
	populated_structure_solutions(solution_space, test_map, N)
	time1 = time_last = clock()
	print "Find structure", int((time1 - time0) * 10) * 0.1
	print solution_space.get_printable_status()
	next_point = NextPoint(test_map)
	solution_puller = SolutionPuller(solution_space, N, next_point)
	r = 0
	while True: # solution_puller.SUCCESS == False
		r += 1
		solution_puller.pull_down()
		solution_puller.pull_up()
		if clock() - time_last > 30:
			time_last = clock()
			print "ROUND", r, "ELAPSED", int((clock() - time0) * 10) * 0.1
			print solution_space.get_printable_status(), solution_puller.LEVEL
		if clock() - time0 > 6000 or solution_space.SUCCESS:
			print solution_space.get_printable_status()
			break
