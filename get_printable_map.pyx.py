def get_printable_map(test_map):
	ans = '\n'.join([''.join(line) for line in test_map])
	ans = ans.replace('0', ' ')
	ans = ans.replace('2', 'x')
	return ans