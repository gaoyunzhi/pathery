S = "S"
E = "E"
B = "1"
O = "0"

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def in_boundary(x, y, L, W):
	return 0 <= x < L and 0 <= y < W

def get_dis_map(test_map, start, end, L, W)
	dis_map = [[-1] * W for _ in xrange(L)]
	queue = []
	for i in xrange(L):
		for j in xrange(W):
			if test_map[i][j] == S:
				queue.add((i, j))
	p = 0 
	distance = -1
	while p < len(queue):
		if dis_map[x][y] == distance:
			break
		for dx, dy in DIRECTION:
			x, y = queue[p]
			nx, ny = x + dx, y + dy
			if not in_boundary(nx, ny, L, W):
				continue
			if dis_map[nx][ny] == -1 and test_map[nx][ny] == O: 
				queue.add((nx, ny))
				dis_map[nx][ny] = dis_map[x][y] + 1
				if test_map[nx][ny] == E:
					distance = dis_map[nx][ny]
		p += 1
	return dis_map, distance

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
			if start_map[i][j] + end_map[i][j] == dis:
				current_dis = start_map[i][j]
				path_map[current_dis] = path_map.get(current_dis, set())
				path_map[current_dis].add((i, j))
	return path_map, dis
