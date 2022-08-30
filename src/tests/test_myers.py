import pytest
from src.helpers.myers import Myers

@pytest.fixture
def lines():
	a_lines = create_string_list(0, 10)
	b_lines = create_string_list(5, 10)
	return a_lines, b_lines

	# myers = Myers(a_lines, b_lines)
	# myers.print_diff()


def print_list(arr: list):
	for a in arr:
		print(a)

def create_string_list(start, stop):
	return [str(num) for num in range(start, stop)]

def test_delete_first_item(lines):
	""" should delete 10 in a_lines, but that cant
		be distinguished from the rest """

	a_lines, b_lines = lines
	del b_lines[0]

	myers = Myers(a_lines, b_lines)
	myers.print_diff()


def test_appending_and_deleting_last_line(lines):
	""" currently cant distinguish between appending something to a_lines
		and deleting last element from b_lines """
	# b_lines.append('40')
	a_lines, b_lines = lines
	a_lines.append('10')
	del b_lines[-1]

	myers = Myers(a_lines, b_lines)
	myers.print_diff()


def test_diffing_changes_before(lines: list[list]):
	a_lines_before, b_lines_before = lines
	a_lines_after = a_lines_before.copy()
	b_lines_after = b_lines_before.copy()

	a_lines_after.append('10')
	del b_lines_after[-1]

	a_myers = Myers(a_lines_before, a_lines_after)
	a_myers.print_diff()

	b_myers = Myers(b_lines_before, b_lines_after)
	b_myers.print_diff()

