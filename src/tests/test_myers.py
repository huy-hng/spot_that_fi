from dataclasses import dataclass
import pytest
from src.helpers.myers import Element, Myers, Operations


@dataclass
class Params:
	lines: list[int]
	inserts: list[int]
	removals: list[int]
	expected: list[int]

	def change(self):
		return changer(self.lines.copy(), self.inserts, self.removals)

def parameters():
	# should delete 5 in a_lines, but that cant be distinguished from the rest
	# currently cant distinguish between appending something to a_lines and deleting last element from b_lines
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

	a_myers = myers_wrapper(a.lines, a_after)
	b_myers = myers_wrapper(b.lines, b_after)
	ab_myers = myers_wrapper(a_after, b_after)

	a_myers.print_diff('a_lines')
	b_myers.print_diff('b_lines')
	ab_myers.print_diff('a/b')

	a_result = changer(a_after, b_myers.inserts, b_myers.removals)
	b_result = a_result[-5:]
	# b_result = changer(b_after, a_myers.inserts, a_myers.removals)
	print(a.inserts, a.removals)
	print(b.inserts, b.removals)

	assert a_result == a.expected
	assert b_result == b.expected

	
def changer(lines: list[int], inserts: list[int], removals: list[int]):
	for insert in inserts:
		lines.append(insert)
	for remove in removals:
		if remove in lines:
			lines.remove(remove)
		else:
			print(f'skipping {remove}')
	return lines


def myers_wrapper(a_lines: list[int], b_lines: list[int]):
	convert_int_list = lambda arr: list(map(str, arr))
	convert_str_list = lambda arr: list(map(int, arr))
	myers = Myers(convert_int_list(a_lines), convert_int_list(b_lines))
	myers.keeps = convert_str_list(myers.keeps)
	myers.inserts = convert_str_list(myers.inserts)
	myers.removals = convert_str_list(myers.removals)
	return myers
