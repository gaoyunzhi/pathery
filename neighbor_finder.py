O = "0"

class NeighborFinder(object):
	def __init__(self, test_map):
		self.blank = set()
		for x, line in enumerate(test_map):
			for y, c in enumerate(line):
				if c == O:
					self.blank.add((x, y))

	def find(self, solution, p):
		for dx in xrange(-1, 2):
			for dy in xrange(-1, 2):
				np = p[0] + dx, p[1] + dy
				if not np in solution and np in self.blank:
					yield np

