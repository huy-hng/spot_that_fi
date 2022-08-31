import random
from dataclasses import dataclass
import pytest
from src.controller.playlist_change_detection import Diff
from src.helpers.myers import Element, Myers, Operations

def changer(lines: list[int], inserts: list[int], removals: list[int]):
	for insert in inserts:
		lines.append(insert)
	for remove in removals:
		if remove in lines:
			lines.remove(remove)
		else:
			print(f'skipping {remove}')
	return lines


@dataclass
class Params:
	lines: list[int]
	inserts: list[int]
	removals: list[int]
	expected: list[int]

	def change(self):
		return changer(self.lines.copy(), self.inserts, self.removals)

def parameters():
	a_lines = [0,1,2,3,4,5,6,7,8,9]
	b_lines = [5,6,7,8,9]
	return [
		(
			Params(
				a_lines,
				[], [],
				[0,1,2,3,4,6,7,8,9],
			),
			Params(
				b_lines,
				[], [5],
				[4,6,7,8,9]
			)
		),
		(
			Params(
				a_lines,
				[10], [],
				[0,1,2,3,4,5,6,7,8,10]
			),
			Params(
				b_lines,
				[], [9],
				[5,6,7,8,10]
			)
		),
		(
			Params(
				a_lines,
				[10], [0,1],
				[2,3,4,5,6,7,8,9,10],
			),
			Params(
				b_lines,
				[], [],
				[6,7,8,9,10]
			)
		),
		(
			Params(
				a_lines,
				[], [],
				[0,1,2,3,4,5,6,7,8,9,10],
			),
			Params(
				b_lines,
				[10], [],
				[6,7,8,9,10]
			)
		),
		(
			Params(
				a_lines,
				[], [9],
				[0,1,2,3,4,5,6,7,8],
			),
			Params(
				b_lines,
				[], [9],
				[4,5,6,7,8]
			)
		),
	]


@pytest.mark.parametrize('a,b', parameters())
def test_syncing_of_two_playlists(a: Params, b: Params):
	""" tests two playlists that are independently
		of each other able to change """

	snippet_size = 5

	a_after = a.change()
	b_after = b.change()

	a_myers = Myers(a.lines, a_after)
	b_myers = Myers(b.lines, b_after)
	ab_myers = Myers(a_after, b_after)

	Myers.print_groups(
		a_myers.get_vis_diff('a_lines'),
		b_myers.get_vis_diff('b_lines'),
		ab_myers.get_vis_diff('ab_lines'),
		group_size=3
	)

	a_result = changer(a_after, b_myers.inserts, b_myers.removals)
	b_result = a_result[-5:]
	# b_result = changer(b_after, a_myers.inserts, a_myers.removals)
	print(a.inserts, a.removals)
	print(b.inserts, b.removals)

	assert a_result == a.expected
	assert b_result == b.expected

	
def random_input():
	total = 20
	lines = list(range(total))

	num_removals = random.randint(0,int(total/2))
	removals = []
	for _ in range(num_removals):
		delete = random.randint(0, len(lines)-1)
		removals.append(lines[delete])
		del lines[delete]
	removals.sort()

	# num_insertions = random.randint(0,int(total/2))
	# start_int = total
	# insertions = [insertion for insertion in range(total, total+num_insertions)]
	# for _ in range(num_insertions):
	# 	lines.append(start_int)
	# 	start_int += 1

	return lines, [], removals


def not_random_input():
	total = 20
	lines = list(range(total))
	# removals = lines[15:]
	removals = [lines[5]]
	[lines.remove(r) for r in removals]
	return lines, [], removals


@pytest.mark.parametrize('new_lines,inserts,removals',
	[random_input() for _ in range(1)])
	# [not_random_input()])
def test_find_earliest_keep(new_lines,inserts,removals):
	""" testing algorithm for database update\n
		only b_lines (playlist tracks on spotify side) can be changed\n
		inserts can only be at the end and removals can be anywhere
	"""

	limit = 5

	old_lines = list(range(20))
	groups = grouper(new_lines, limit)
	expected_length = len(new_lines)
	
	diffs: list[list[str]] = []
	saved_lines = []
	myers = Myers(old_lines, saved_lines)
	# myers = Myers()
	broke = False
	for i, group in enumerate(groups):
		""" actual logic """
		saved_lines = group + saved_lines

		myers = Myers(old_lines, saved_lines)
		diffs.append(myers.get_vis_diff(str(i)))

		if myers.keeps:
			first_keep_index = old_lines.index(myers.keeps[0])
			estimated_total = first_keep_index + len(saved_lines)
			if estimated_total == expected_length:
				broke = True
				break

	if broke:
		first_keep_index = old_lines.index(myers.keeps[0])
	else:
		first_keep_index = 0
		estimated_total = len(saved_lines)
	
	
	ins = []
	rem = []
	for line, operation in myers.diff[first_keep_index:]:
		if operation == Operations.Insert:
			ins.append(line)
		elif operation == Operations.Remove:
			rem.append(line)

	Myers.print_groups(*diffs, group_size=4, distance=5)
	# print(f'{estimated_total} | {expected_length} | {len(saved_lines)}')
	print(f'{saved_lines=}')
	# print(f'{inserts=}')
	# print(f'{ins=}')
	# print()
	print(f'{removals=}')
	# print(f'{rem=}')

	assert estimated_total == expected_length
	assert inserts == ins
	assert removals == rem

	# assert len(saved_lines) == expected_length


def grouper(new_lines, limit):
	new_lines.reverse()
	groups = [new_lines[n:n+limit] for n in range(0, len(new_lines), limit)]
	[group.reverse() for group in groups]
	return groups