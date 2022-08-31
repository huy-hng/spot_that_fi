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

	# b_lines = list(range(5, 20))
	
	size = 4
	curr = 20

	diffs: list[list[str]] = []
	a_lines = list(range(curr))
	while curr>0:
		curr -= size
		b_lines = list(range(curr, curr+size))

		myers = Myers(a_lines, b_lines)
		diffs.append(myers.get_vis_diff(str(curr)))

	Myers.print_groups(*diffs, group_size=3, distance=2)
