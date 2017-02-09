from random import random
EPSILON = 0.00000000001

def get_weighted_random(distribution):
	range_map = {}
	start = 0.0
	for key in distribution:
		range_map[key] = (start, start + distribution[key])
		start += distribution[key]
	draw = random() * start
	for key in distribution:
		if range_map[key][0] - EPSILON <= draw <= range_map[key][1] - EPSILON:
			return key
	raise Exception("Error when drawing number")