from random import shuffle, randint
ROUND = 100

class SolutionPuller(object):
	def __init__(self, solution_space, N, next_point):
		self.solution_space = solution_space
		self.N = N
		self.LEVEL = 0
		self.SUCCESS = False
		self.next_point = next_point
		self.did_nothing_time = 0

	def shuffle(self, aList):
		weight = len(aList) / ROUND
		if weight % 5 == 4 and randint(0, weight / 10) == 0:
			shuffle(aList)

	def pull_down(self):
		did_nothing = True
		for n in xrange(self.N, 1, -1):
			dis = self.solution_space.best[n] - self.LEVEL
			if not dis in self.solution_space.to_pulldown[n]:
				continue
			r = 0
			self.shuffle(self.solution_space.to_pulldown[n][dis])
			while self.solution_space.to_pulldown[n][dis] and r < ROUND:
				r += 1
				did_nothing = False
				solution = self.solution_space.to_pulldown[n][dis].pop(0)
				for p in solution:
					n_solution = set(solution)
					n_solution.remove(p)
					new_level, self.SUCCESS = self.solution_space.addSafe(n_solution)
					if new_level < self.LEVEL:
						self.LEVEL = new_level
						self.updateDidNothing(False)
						return # stop pull down
		self.updateDidNothing(did_nothing)

	def pull_up(self):
		did_nothing = True
		for n in xrange(self.N):
			dis = self.solution_space.best[n] - self.LEVEL
			if not dis in self.solution_space.to_expand[n]:
				continue
			r = 0
			while self.solution_space.to_expand[n][dis] and r < ROUND:
				r += 1
				did_nothing = False
				solution = self.solution_space.to_expand[n][dis].pop(0)
				for p in self.next_point.get(solution):
					n_solution = set(solution)
					n_solution.add(p)
					new_level, self.SUCCESS = self.solution_space.addSafe(n_solution)
					if new_level < self.LEVEL:
						self.LEVEL = new_level
						self.updateDidNothing(False)
						return # stop pull up
		self.updateDidNothing(did_nothing)

	def updateDidNothing(self, did_nothing):
		if did_nothing:
			self.did_nothing_time += 1
			if self.did_nothing_time >= 2:
				self.did_nothing_time = 0
				self.LEVEL += 1
		else:
			self.did_nothing_time = 0