import re

def parse_raw(f):
	with open(f, 'r') as file:
		content = file.read()
	num = re.findall(">[0-9]+ walls<", content)
	num = num[0][1: -7]
	score = re.findall('[0-9]+<\/a><\/td><td style=\"text-align:right;\">', content)
	if score:
		score = score[0][:-39]
	if not score:
		score = re.findall(">[0-9]+<\/td><\/tr><tr class=\"scoreRow1", content)
		score = score[0][1:-30]
	map_id = re.findall("resetwalls\([0-9]+\)", content)
	map_id = map_id[0][11: -1]
	L = len(re.findall(map_id + ",.,0", content)) / 2
	test_map = re.findall("mapcell .[0-9]*", content)
	test_map_new = []
	for x in test_map:
		if len(x) == 9:
			test_map_new.append(x[-1])
			continue
		test_map_new.append(chr(int(x[-1]) + ord('A') - 1))
	test_map = test_map_new
	size = len(test_map)
	W = size / L
	test_map_new = []
	c = 0
	for x in test_map:
		test_map_new.append(x)
		c += 1
		if c == W:
			test_map_new.append('\n')
			c = 0
	test_map_new = ''.join(test_map_new)
	test_map_new = test_map_new.replace('o', '0')
	test_map_new = test_map_new.replace('s', 'S')
	test_map_new = test_map_new.replace('f', 'E')
	test_map_new = test_map_new.replace('r', '1')
	test_map_new = test_map_new.replace('c', 'A')
	return num + '\n' + score + '\n' + test_map_new.strip()