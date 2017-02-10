from get_printable_map import get_printable_map
S = "S"
E = "E"
B = "1"
O = "0"

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def in_boundary(x, y, L, W):
	return 0 <= x < L and 0 <= y < W

def get_dis_map(test_map, start, end, L, W):
	dis_map = [[-1] * W for _ in xrange(L)]
	queue = []
	for x in xrange(L):
		for y in xrange(W):
			if test_map[x][y] == start:
				queue.append((x, y))
				dis_map[x][y] = 0
	p = 0 
	distance = -1
	while p < len(queue):
		x, y = queue[p]
		if dis_map[x][y] == distance:
			break
		for dx, dy in DIRECTION:
			nx, ny = x + dx, y + dy
			if not in_boundary(nx, ny, L, W):
				continue
			if dis_map[nx][ny] == -1 and test_map[nx][ny] in [O, S, E]: 
				queue.append((nx, ny))
				dis_map[nx][ny] = dis_map[x][y] + 1
				if test_map[nx][ny] == end:
					distance = dis_map[nx][ny]
		p += 1
	return dis_map, distance

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
	start_map, _ = get_dis_map(test_map, S, E, L, W)
	end_map, dis = get_dis_map(test_map, E, S, L, W)
	if dis == -1:
		return {}, -1
	path_map = {}
	for i in xrange(L):
		for j in xrange(W):
			if start_map[i][j] + end_map[i][j] == dis and test_map[i][j] == O:
				current_dis = start_map[i][j]
				path_map[current_dis] = path_map.get(current_dis, set())
				path_map[current_dis].add((i, j))
	contangent_points = get_contangent_points(test_map, L, W)
	for d in path_map:
		path_map[d] &= contangent_points
	return path_map, dis
