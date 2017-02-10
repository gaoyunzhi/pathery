from random import random
EPSILON = 0.00000000001

def get_weighted_random(choice, probability_space):
	range_map = {}
	start = 0.0
	for x, y in choice:
		range_map[(x, y)] = (start, start + probability_space[x][y])
		start += probability_space[x][y]
	draw = random() * start
	for key in choice:
		if range_map[key][0] - EPSILON <= draw <= range_map[key][1] - EPSILON:
			return key
	raise Exception("Probalistic draw fail")