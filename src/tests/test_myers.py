from dataclasses import dataclass
import pytest
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

	
def test_find_earliest_keep():
	""" testing algorithm for database update\n
		only b_lines (playlist tracks on spotify side) can be changed\n
		inserts can only be at the end and removals can be anywhere
	"""

	total_size = 20

	old_lines = list(range(total_size))
	new_lines = old_lines.copy()

	del new_lines[-4:]
	del new_lines[0:7]
	# del new_lines[0]
	# new_lines.append(20)
	new_lines += list(range(20,27))


def earliest_keep_helper(old_lines, new_lines):
	limit = 5

	expected_length = len(new_lines)
	new_lines.reverse()
	groups = [new_lines[n:n+limit] for n in range(0, expected_length, limit)]
	[group.reverse() for group in groups]

	diffs: list[list[str]] = []
	print(f'{expected_length = }\n')
	
	saved_lines = []
	estimated_length = 0
	for iteration, group in enumerate(groups):
		""" actual logic """
		saved_lines = group + saved_lines

		myers = Myers(old_lines, saved_lines)
		diffs.append(myers.get_vis_diff(str(iteration)))

		if myers.keeps: # algorithm to save on iterations
			# first_keep_index = old_lines.index(myers.keeps[0])
			# estimated_length = first_keep_index + len(saved_lines)
			# print(f'{first_keep_index} {len(saved_lines)} = {estimated_length}')
			print(len(saved_lines))
			# if estimated_length == expected_length:
			if len(saved_lines) == expected_length:
				break

	# if estimated_length != expected_length:
	# 	first_keep_index = 0
	# 	estimated_length = first_keep_index + len(saved_lines)

	Myers.print_groups(*diffs, group_size=4, distance=5)

	assert len(saved_lines) == expected_length