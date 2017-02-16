from apply_solution import apply_solution
from in_boundary import in_boundary
DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]

S = "S"
E = "E"
V = "1"
O = "0"
A = "A"
U = "2"

class DisFinder(object):
	def __init__(self, test_map):
		self.test_map = test_map
		self.L = L = len(test_map)
		self.W = W = len(test_map[0])
		
		middle_points = []
		for x in xrange(L):
			for y in xrange(W):
				if test_map[x][y] not in [S, E, O, V, U]:
					middle_points.append(test_map[x][y])
		middle_points.sort()
		middle_points = [S] + middle_points + [E]
		middle_points_map = {}
		for x in xrange(L):
			for y in xrange(W):
				c = test_map[x][y]
				if c not in [O, V, U]:
					middle_points_map[c] = middle_points_map.get(c, set())
					middle_points_map[c].add((x, y))
		self.middle_points = [middle_points_map[c] for c in middle_points]
	
	def find_part_dis(self, test_map, begins, ends):
		visited = set(begins)
		dis = 1
		queue = begins
		while queue:
			n_queue = []
			for x, y in queue:
				for dx, dy in DIRECTION:
					nx, ny = x + dx, y + dy
					if (nx, ny) in ends:
						return dis
					if not in_boundary(nx, ny, self.L, self.W):
						continue
					if test_map[nx][ny] != V \
						and test_map[nx][ny] != U and not (nx, ny) in visited: 
						n_queue.append((nx, ny))
						visited.add((nx, ny))
			dis += 1
			queue = n_queue
		return -1

	def get(self, solution):
		test_map = apply_solution(self.test_map, solution)
		totol_dis = 0
		for index in xrange(len(self.middle_points) - 1):
			part_dis = self.find_part_dis(test_map, self.middle_points[index], self.middle_points[index + 1])
			if part_dis == -1:
				return -1
			totol_dis += part_dis
		return totol_dis