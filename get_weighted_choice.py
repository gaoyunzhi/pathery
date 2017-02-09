W = 0.25

def get_weighted_choice(path_map):
	choice = {}
	for d, uniform_set in path_map.iteritems():
		w = W ** len(uniform_set)
		for p in uniform_set:
			choice[p] = w
	return choice