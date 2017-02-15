from apply_solution import apply_solution
from get_solution_hash import get_solution_hash
from find_dis import find_dis

class SolutionSpace(object):
	def __init__(self, test_map, N, ANS):
		self.ANS = ANS
		self.best_solution = None
		self.best = {}
		self.to_expand = {}
		self.to_pulldown = {}
		for x in xrange(N + 1):
			self.to_expand[x] = {}
			self.to_pulldown[x] = {}
		self.visited = set()
		self.next_points = {}
		self.test_map = test_map

	def add(self, solution):
		solution_hash = get_solution_hash(solution)
		if solution_hash in self.visited:
			raise Exception("solution already added")
		self._add(solution, solution_hash)

	def addSafeWithHash(self, solution, solution_hash):
		if solution_hash in self.visited:
			return
		self._add(solution, solution_hash)

	def _add(self, solution, solution_hash):
		dis = find_dis(apply_solution(self.test_map, solution))
		n = len(solution)
		if not dis in self.to_expand[n]:
			self.to_expand[n][dis] = []
		self.to_expand[n][dis].append(solution)
		self.visited.add(solution_hash)
		if dis > self.best.get(n, 0):
			self.best[n] = dis
		return self.best[n] - dis, dis == self.ANS

	def has(self, solution):
		return solution in self.visited





