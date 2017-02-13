def convert_accompany_space(accompany_space):
	result = {}
	for p1 in accompany_space:
		result[p1] = sorted(
			accompany_space[p1].keys(), 
			key=lambda p2: accompany_space[p1][p2], 
			reverse=True)[:3]
	return result