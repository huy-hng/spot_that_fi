from dataclasses import dataclass
import pytest
from src.helpers.myers import Element, Myers, Operations

def test_delete_first_item(lines):

	a_lines, b_lines = lines
	del b_lines[0]

	myers = Myers(a_lines, b_lines)
	myers.print_diff()


def test_appending_and_deleting_last_line(lines):
	# b_lines.append('40')
	a_lines: list = lines[0]
	b_lines: list = lines[1]

	a_lines = changer(a_lines, [10], [])
	b_lines = changer(b_lines, [], [9])

	myers = myers_wrapper(a_lines, b_lines)
	myers.print_diff()


@dataclass
class Params:
	lines: list[int]
	inserts: list[int]
	removals: list[int]
	expected: list[int]

	def change(self):
		lines = self.lines.copy()
		for insert in self.inserts:
			lines.append(insert)
		for remove in self.removals:
			lines.remove(remove)
		return lines

@dataclass
class Parameters:
	a_before: list[int]
	a_after: list[int]
	a_inserts: list[int]
	a_removals: list[int]

	b_before: list[int]
	b_after: list[int]
	b_inserts: list[int]
	b_removals: list[int]



def parameters():
	# should delete 5 in a_lines, but that cant be distinguished from the rest
	# currently cant distinguish between appending something to a_lines and deleting last element from b_lines
	return [
		(
			Params(
				[0,1,2,3,4],
				[], [],
				[0,1,2,4],
			),
			Params(
				[3,4],
				[], [3],
				[4]
			)
		),
		(
			Params(
				[0,1,2,3,4],
				[5], [],
				[0,1,2,3,5],
			),
			Params(
				[3,4],
				[], [4],
				[3,5]
			)
		),
		(
			Params(
				[0,1,2,3,4],
				[5], [0,1],
				[2,3,4,5],
			),
			Params(
				[3,4],
				[], [],
				[3,4,5]
			)
		)
		# Parameters(
		# 	[0,1,2,3,4],
		# 	[0,1,2,3,4,5],
		# 	[5], [],

		# 	[3,4],
		# 	[3],
		# 	[], [4]
		# ),
	]
	# return [
	# 	([], [], [], [5]), 
	# 	([10], [], [], [5]),
	# 	([10], [], [], [9]), 
	# ]


@pytest.mark.parametrize('a,b', parameters())
def test_diffing_changes_before(a: Params, b: Params):

	a_after = a.change()
	b_after = b.change()

	a_myers = myers_wrapper(a.lines, a_after)
	b_myers = myers_wrapper(b.lines, b_after)
	ab_myers = myers_wrapper(a_after, b_after)

	a_myers.print_diff('a_lines')
	b_myers.print_diff('b_lines')
	ab_myers.print_diff('a/b')

	a_result = changer(a_after, b_myers.inserts, b_myers.removals)
	b_result = changer(b_after, a_myers.inserts, a_myers.removals)
	print(a_result)
	print(b_result)

	assert a_result == a.expected
	assert b_result == b.expected

	
def changer(lines: list[int], inserts: list[int], removals: list[int]):
	for insert in inserts:
		lines.append(insert)
	for remove in removals:
		if remove in lines:
			lines.remove(remove)
	return lines


def myers_wrapper(a_lines: list[int], b_lines: list[int]):
	convert_int_list = lambda arr: list(map(str, arr))
	convert_str_list = lambda arr: list(map(int, arr))
	myers = Myers(convert_int_list(a_lines), convert_int_list(b_lines))
	myers.keeps = convert_str_list(myers.keeps)
	myers.inserts = convert_str_list(myers.inserts)
	myers.removals = convert_str_list(myers.removals)
	return myers


@pytest.fixture
def lines():
	a_lines = list(range(10))
	b_lines = list(range(5, 10))
	return a_lines, b_lines


