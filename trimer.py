V = "1"
from in_boundary import in_boundary
DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Trimer(object):
	def __init__(self, test_map):
		self.test_map = test_map
		L = self.L = len(test_map)
		W = self.W = len(test_map[0])
		self.blockers = set()
		for x in xrange(L):
			for y in xrange(W):
				if test_map[x][y] == V:
					self.blockers.add((x, y))

	def trim(self, solution):
		to_trim = set()
		for x, y in solution:
			num_blocker = 0
			for dx, dy in DIRECTION:
				np = nx, ny = x + dx, y + dy
				if not in_boundary(nx, ny, self.L, self.W):
					num_blocker += 1
					continue
				if np in self.blockers or np in solution:
					num_blocker += 1
			if num_blocker > 2:
				to_trim.add((x, y))
		if to_trim:
			solution -= to_trim
			return True
		return False



