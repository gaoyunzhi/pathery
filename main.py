import sys
from const import TEST_DIRECTORY
from read_map import read_map
from find_solution import find_solution
from os import walk
from parse_raw import parse_raw

def main(arg):
	all_filenames = []
	for (dirpath, dirnames, filenames) in walk(TEST_DIRECTORY):
		for fn in filenames:
			all_filenames.append((dirpath, fn))

	all_filenames = [(d, f) for (d, f) in all_filenames if f.endswith('.txt')]

	for d, f in all_filenames:
		if f.startswith('raw_'):
			new_f = d + f[4:]
			with open(new_f, 'w') as nf:
				nf.write(parse_raw(d + f))

	for d, f in all_filenames:
		if not f.startswith(arg):
			continue
		test_map, num, ans = read_map(d + f)
		find_solution(test_map, num, ans)
		break