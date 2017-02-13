def read_map(example_file):
	with open(example_file) as f:
		raw_map = f.readlines()
	num = int(raw_map.pop(0))
	print "===", num
	ans = int(raw_map.pop(0))
	print "===", ans
	test_map = [line.strip() for line in raw_map]
	print "===", test_map
	return [line for line in test_map if line], num, ans
