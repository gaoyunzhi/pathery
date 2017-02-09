from const import TEST_DIRECTORY
from read_map import read_map
from find_solution import find_solution
from os import walk

all_filenames = []
for (dirpath, dirnames, filenames) in walk(TEST_DIRECTORY):
	for fn in filenames:
		all_filenames.append((dirpath, fn))

all_filenames = [d + f for (d, f) in all_filenames if f.endswith('.txt')]

for file in all_filenames:
	test_map, num = read_map(file)
	for x in find_solution(test_map, num):
		print x
