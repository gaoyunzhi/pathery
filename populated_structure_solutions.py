from in_boundary import in_boundary
V = "1"
O = "0"
from get_printable_map import get_printable_map
from get_solution_hash import get_solution_hash

class Structure(object):
	def __init__(self, test_map, solution_space, N):
		self.N = N
		self.solution_space = solution_space
		self.test_map = test_map
		L = len(test_map)
		W = len(test_map[0])
		self.L, self.W = L, W
		self.expanded = set()
		self.components = [set([(-1, x) for x in xrange(0, W)])]
		self.expand(self.components[0])
		self.components.append(set([(L, x) for x in xrange(0, W)]))
		self.expand(self.components[1])
		for i in xrange(L):
			for j in xrange(W):
				if test_map[i][j] == V and not (i, j) in self.expanded:
					self.components.append(set([(i,j)]))
					self.expand(self.components[-1])
		self.dis_map = [{} for _ in self.components]
		print self.mark_components()
		self.tangent_map = {}
		self.tangents = [set() for _ in self.components]
		for index, component in enumerate(self.components):
			self.compute_dis_map(self.dis_map[index], component, index)
		# print self.tangent_map
		self.compute_path()
		self.paths.sort(reverse=True)

	def find_structure_external(self):
		self.visited_structure = set()
		self.find_structure(-1, [set([0, 1])], set())

	def find_structure(self, index, disjoint_set, solution):
		for i in xrange(index + 1, len(self.paths)):
			path_len, points, tangent = self.paths[i]
			if path_len + len(solution) > self.N:
				continue
			if points & solution:
				continue
			n_disjoint_set, is_valid = self.get_disjoint_set(disjoint_set, tangent)
			if not is_valid:
				continue
			n_solution = set(solution)
			n_solution.update(points)
			solution_hash = get_solution_hash(n_solution)
			if solution_hash in self.visited_structure:
				continue
			self.solution_space.addSafeWithHash(n_solution, solution_hash)
			self.find_structure(i + 1, n_disjoint_set, n_solution)

	def get_disjoint_set(self, disjoint_set, tangent):
		connected = set(tangent)
		n_disjoint_set = []
		for component in disjoint_set:
			join_points = component & tangent
			if len(join_points) > 1:
				return None, False
			if len(join_points) == 1:
				connected.update(component)
			else:
				n_disjoint_set.append(component)
		n_disjoint_set.append(connected)
		return n_disjoint_set, True

	def compute_path(self):
		n = len(self.components)
		self.paths = []
		self.paths_dedup = set()
		for i in xrange(n):
			for j in xrange(max(i + 1, 2), n):
				dis, starts = self.get_dis(self.tangents[i], self.dis_map[j])
				for s in starts:
					self.search_path(i, j, 1, dis - 2, set([s]), s, set([i, j]))

	def search_path(self, i, j, d1, d2, points, p, connects):
		if d2 == -1:
			path_hash = get_solution_hash(points)
			if path_hash in self.paths_dedup:
				return
			self.paths_dedup.add(path_hash)
			self.paths.append((len(points), points, connects))
			return
		x, y = p
		for dx in xrange(-1, 2):
			for dy in xrange(-1, 2):
				nx = dx + x
				ny = dy + y
				np = (nx, ny)
				if in_boundary(nx, ny, self.L, self.W) and \
					self.dis_map[i].get(np, -2) == d1 and \
					self.dis_map[j].get(np, -2) == d2:
					npoints = set(points)
					npoints.add(np)
					nconnects = set(connects)
					nconnects.update(self.tangent_map.get(np, set()))
					self.search_path(i, j, d1 + 1, d2 - 1, npoints, np, nconnects)

	def get_dis(self, tangents, dis_map):
		dis = min([dis_map[p] for p in tangents])
		starts = [p for p in tangents if dis_map[p] == dis]
		return dis + 1, starts
	
	def compute_dis_map(self, dis_map, component, index):
		queue = []
		p = 0
		for x, y in component:
			dis_map[(x, y)] = -1
			queue.append((x, y))
		while p < len(queue):
			x, y = queue[p]
			for dx in xrange(-1, 2):
				for dy in xrange(-1, 2):
					nx = x + dx
					ny = y + dy
					if in_boundary(nx, ny, self.L, self.W) and \
						not (nx, ny) in dis_map and self.test_map[nx][ny] == O:
						dis_map[(nx, ny)] = dis_map[(x, y)] + 1
						queue.append((nx, ny))
						if dis_map[(nx, ny)] == 0:
							if not (nx, ny) in self.tangent_map:
								self.tangent_map[(nx, ny)] = set()
							self.tangent_map[(nx, ny)].add(index)
							self.tangents[index].add((nx, ny))
			p += 1

	def mark_dis_map(self, dis_map):
		test_map = [line[:] for line in self.test_map]
		for x, y in dis_map:
			if in_boundary(x, y, self.L, self.W):
				test_map[x][y] = chr(ord('b') + dis_map[(x, y)])
		return get_printable_map(test_map)

	def mark_components(self):
		test_map = [line[:] for line in self.test_map]
		for index, component in enumerate(self.components):
			for x, y in component:
				if in_boundary(x, y, self.L, self.W):
					test_map[x][y] = chr(ord('a') + index)
		return get_printable_map(test_map)

	def expand(self, component):
		queue = list(component)
		p = 0
		while p < len(queue):
			x, y = queue[p]
			self.expanded.add((x, y))
			for dx in xrange(-1, 2):
				for dy in xrange(-1, 2):
					nx = x + dx
					ny = y + dy
					if in_boundary(nx, ny, self.L, self.W) and \
						not (nx, ny) in self.expanded and self.test_map[nx][ny] == V:
						self.expanded.add((nx, ny))
						component.add((nx, ny))
						queue.append((nx, ny))
			p += 1

def populated_structure_solutions(solution_space, test_map, N):
	structure = Structure(test_map, solution_space, N)
	structure.find_structure_external()