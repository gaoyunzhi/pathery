from in_boundary import in_boundary
O = "0"

def next_points(test_map):
	L = len(test_map)
	W = len(test_map[0])
	next_points = set()
	for x in xrange(L):
		for y in xrange(W):
			if not test_map[x][y] == O:
				continue
			for dx in xrange(-1, 2):
				for dy in xrange(-1, 2):
					nx, ny = x + dx, y + dy
					if not in_boundary(nx, ny, L, W) or test_map[nx][ny] != O:
						next_points.add((x, y))	
	return next_points

