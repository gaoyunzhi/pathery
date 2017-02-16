from random import shuffle, randint
ROUND = 100

class SolutionPuller(object):
	def __init__(self, solution_space, N, next_point, neighbor_finder):
		self.neighbor_finder = neighbor_finder
		self.solution_space = solution_space
		self.N = N
		self.DOWN_LEVEL = 0
		self.UP_LEVEL = 0
		self.next_point = next_point

	def shuffle(self, aList):
		weight = len(aList) / ROUND
		if weight % 5 == 4 and randint(0, weight / 10) == 0:
			shuffle(aList)

	def pull_down(self):
		things = 0
		for n in xrange(self.N, 1, -1):
			dis = self.solution_space.best[n] - self.DOWN_LEVEL
			if not dis in self.solution_space.to_pulldown[n]:
				continue
			r = 0
			self.shuffle(self.solution_space.to_pulldown[n][dis])
			while self.solution_space.to_pulldown[n][dis] and r < ROUND:
				r += 1
				things = max(1, things)
				solution = self.solution_space.to_pulldown[n][dis].pop(0)
				for p in solution:
					n_solution = set(solution)
					n_solution.remove(p)
					new_level, result = self.solution_space.add(n_solution)
					if result != None:
						things += 1
					if new_level < self.DOWN_LEVEL:
						self.DOWN_LEVEL = new_level
						return # stop pull down
		if things == 0:
			self.DOWN_LEVEL += 1
		if randint(0, ROUND * self.N * 10) < things:
			self.UP_LEVEL = min(self.UP_LEVEL, self.DOWN_LEVEL)

	def pull_up(self):
		things = 0
		for n in xrange(self.N):
			dis = self.solution_space.best[n] - self.UP_LEVEL
			if not dis in self.solution_space.to_expand[n]:
				continue
			r = 0
			while self.solution_space.to_expand[n][dis] and r < ROUND:
				r += 1
				things = max(1, things)
				solution = self.solution_space.to_expand[n][dis].pop(0)
				for p in self.next_point.get(solution):
					n_solution = set(solution)
					n_solution.add(p)
					new_level, result = self.solution_space.add(n_solution)
					if result != None:
						things += 1
					if new_level < self.UP_LEVEL:
						self.UP_LEVEL = new_level
						return # stop pull up
				for p in solution:
					for p1 in self.neighbor_finder.find(solution, p):
						n_solution = set(solution)
						n_solution.remove(p)
						n_solution.add(p1)
						new_level, result = self.solution_space.add(n_solution)
						if result != None:
							things += 1
						if new_level < self.UP_LEVEL:
							self.UP_LEVEL = new_level
							return # stop pull up
		if things == 0:
			self.UP_LEVEL += 1
		if randint(0, ROUND * self.N * 10) < things:
			self.DOWN_LEVEL = min(self.UP_LEVEL, self.DOWN_LEVEL)