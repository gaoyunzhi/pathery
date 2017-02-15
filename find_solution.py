from time import clock
from solution_space import SolutionSpace
from populated_structure_solutions import populated_structure_solutions
from solution_puller import SolutionPuller
from next_point import NextPoint

def find_solution(test_map, N, ANS):
	time0 = clock()
	solution_space = SolutionSpace(test_map, N, ANS)
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
		print "PULL_DOWN", int((clock() - time_last) * 10) * 0.1, "ELAPSED", int((clock() - time0) * 10) * 0.1
		time_last = clock()
		solution_puller.pull_up()
		print "PULL_UP", int((clock() - time_last) * 10) * 0.1, "ELAPSED", int((clock() - time0) * 10) * 0.1
		print solution_space.get_printable_status(), solution_puller.LEVEL
		time_last = clock()
		if clock() - time0 > 600 or solution_space.SUCCESS:
			break
