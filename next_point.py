from get_next_points import next_points 
from in_boundary import in_boundary
O = "0"

class NextPoint(object):
	def __init__(self, test_map):
		self.map_next_points = next_points(test_map)
		self.test_map = test_map
		self.L = len(self.test_map)
		self.W = len(self.test_map[0])

	def get(self, solution):
		ans = set(self.map_next_points)
		for p in solution:
			for dx in xrange(-1, 2):
				for dy in xrange(-1, 2):
					np = nx, ny = p[0] + dx, p[1] + dy
					if in_boundary(nx, ny, self.L, self.W) and self.test_map[nx][ny] == O:
						ans.add(np)
		ans -= solution
		return ans

