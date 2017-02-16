from apply_solution import apply_solution
from get_solution_hash import get_solution_hash
from find_dis import find_dis
from get_printable_map import get_printable_map
from trimer import Trimer

MAX_LEVEL = 10000
class SolutionSpace(object):
	def __init__(self, test_map, N, ANS, dis_finder):
		self.trimer = Trimer(test_map)
		self.ANS = ANS
		self.best_solution = None
		self.best = {}
		self.to_expand = {}
		self.to_pulldown = {}
		for x in xrange(N + 1):
			self.to_expand[x] = {}
			self.to_pulldown[x] = {}
			self.best[x] = 0
		self.visited = set()
		self.next_points = {}
		self.test_map = test_map
		self.N = N
		self.SUCCESS = False
		self.dis_finder = dis_finder

	def add(self, solution):
		solution_hash = get_solution_hash(solution)
		if solution_hash in self.visited:
			return MAX_LEVEL, None
		trimed = self.trimer.trim(solution)
		if trimed:
			self.visited.add(solution_hash)
			solution_hash = get_solution_hash(solution)
			if solution_hash in self.visited:
				return MAX_LEVEL, None
		return self._add(solution, solution_hash)

	def _add(self, solution, solution_hash):
		dis = self.dis_finder.get(solution)
		n = len(solution)
		if dis == -1:
			self.visited.add(solution_hash)
			return MAX_LEVEL, None
		if not dis in self.to_expand[n]:
			self.to_expand[n][dis] = []
			if dis in self.to_pulldown[n]:
				raise Exception("pulldown pull up inconsistency")
			self.to_pulldown[n][dis] = []
		self.to_expand[n][dis].append(solution)
		self.to_expand[n][dis].append(solution)
		self.visited.add(solution_hash)
		if dis > self.best.get(n, 0):
			self.best[n] = dis
			if n == self.N:
				self.best_solution = solution
			if dis == self.ANS:
				self.SUCCESS = True
		return self.best[n] - dis, dis == self.ANS

	def has(self, solution):
		return solution in self.visited

	def get_printable_status(self):
		res = []
		for num in sorted(self.to_expand):
			if not self.to_expand[num].keys():
				continue
			dis = max(self.to_expand[num].keys())
			res.append((num, dis, len(self.to_expand[num][dis])))
		solution = None
		if self.best_solution:
			solution = get_printable_map(apply_solution(self.test_map, self.best_solution))
		return '\n'.join([str(x) for x in [solution, res, self.best]])
