from dataclasses import dataclass
import pytest
from src.helpers.myers import Myers

def test_delete_first_item(lines):
	""" should delete 5 in a_lines, but that cant
		be distinguished from the rest """

	a_lines, b_lines = lines
	del b_lines[0]

	myers = Myers(a_lines, b_lines)
	myers.print_diff()


def test_appending_and_deleting_last_line(lines):
	""" currently cant distinguish between appending something to a_lines
		and deleting last element from b_lines """
	# b_lines.append('40')
	a_lines: list = lines[0]
	b_lines: list = lines[1]

	a_lines = changer(a_lines, [10], [])
	b_lines = changer(b_lines, [], [9])

	myers = myers_wrapper(a_lines, b_lines)
	myers.print_diff()


@dataclass
class Changes:
	a_inserts: list[int]
	a_removals: list[int]
	b_inserts: list[int]
	b_removals: list[int]

def parameters():
	return [
		Changes([10], [], [], [5]),
		Changes([10], [], [], [9])
	]

@pytest.mark.parametrize('changes', parameters())
def test_diffing_changes_before(lines: list[list], changes: Changes):
	print(changes)
	a_lines_before, b_lines_before = lines
	# a_lines_after = a_lines_before.copy()
	# b_lines_after = b_lines_before.copy()

	a_lines_after = changer(a_lines_before.copy(), changes.a_inserts, changes.a_removals)
	b_lines_after = changer(b_lines_before.copy(), changes.b_inserts, changes.b_removals)

	a_myers = myers_wrapper(a_lines_before, a_lines_after)
	b_myers = myers_wrapper(b_lines_before, b_lines_after)
	ab_myers = myers_wrapper(a_lines_after, b_lines_after)

	a_myers.print_diff('a_lines')
	b_myers.print_diff('b_lines')
	ab_myers.print_diff('a/b')


def changer(lines: list[int], inserts: list[int], removals: list[int]):

	for insert in inserts:
		lines.append(insert)
	for remove in removals:
		lines.remove(remove)

	return lines


def myers_wrapper(a_lines: list[int], b_lines: list[int]):
	convert_int_list = lambda arr: list(map(str, arr))
	return Myers(convert_int_list(a_lines), convert_int_list(b_lines))


@pytest.fixture
def lines():
	a_lines = list(range(10))
	b_lines = list(range(5, 10))
	return a_lines, b_lines


