def read_map(example_file):
	with open(example_file) as f:
		raw_map = f.readlines()
	num = int(raw_map.pop(0))
	ans = int(raw_map.pop(0))
	test_map = [line.strip() for line in raw_map]
	return [list(line) for line in test_map if line], num, ans
