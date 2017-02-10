from get_printable_map import get_printable_map
S = "S"
E = "E"
V = "1"
O = "0"
A = "A"
U = "2"

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def in_boundary(x, y, L, W):
	return 0 <= x < L and 0 <= y < W

def get_contangent_points(test_map, L, W):
	contangent_points = set()
	for x in xrange(L):
		for y in xrange(W):
			if not test_map[x][y] == O:
				continue
			for dx in xrange(-1, 2):
				for dy in xrange(-1, 2):
					nx, ny = x + dx, y + dy
					if not in_boundary(nx, ny, L, W) or test_map[nx][ny] != O:
						contangent_points.add((x, y))	
	return contangent_points

def find_path(test_map):
	L = len(test_map)
	W = len(test_map[0])
	dis = find_dis_all(test_map, L, W)
	if dis == -1:
		return set(), -1
	return get_contangent_points(test_map, L, W), dis

def find_dis_all(test_map, L, W):
	hasA = False
	middle_points = []
	for x in xrange(L):
		for y in xrange(W):
			if test_map[x][y] not in [S, E, O, V, U]:
				middle_points.append(test_map[x][y])
	middle_points.sort()
	middle_points = [S] + middle_points + [E]
	totol_dis = 0
	for index in xrange(len(middle_points) - 1):
		part_dis = \
			find_dis(test_map, L, W, middle_points[index], middle_points[index + 1])
		if part_dis == -1:
			return -1
		totol_dis += part_dis
	return totol_dis

def find_dis(test_map, L, W, start, end):
	dis_map = [[-1] * W for _ in xrange(L)]
	queue = []
	for x in xrange(L):
		for y in xrange(W):
			if test_map[x][y] == start:
				dis_map[x][y] = 0
				queue.append((x, y))
	p = 0 
	while p < len(queue):
		x, y = queue[p]
		for dx, dy in DIRECTION:
			nx, ny = x + dx, y + dy
			if not in_boundary(nx, ny, L, W):
				continue
			if dis_map[nx][ny] == -1 and test_map[nx][ny] != V \
				and test_map[nx][ny] != U: 
				queue.append((nx, ny))
				dis_map[nx][ny] = dis_map[x][y] + 1
				if test_map[nx][ny] == end:
					return dis_map[nx][ny]
		p += 1
	return -1
