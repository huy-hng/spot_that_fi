from enum import Enum
from itertools import zip_longest
from typing import Generic, NamedTuple, TypeVar
from difflib import Differ

from src.utils import allow_generic_namedtuples


allow_generic_namedtuples()
T = TypeVar('T')


class Operations(Enum):
	Keep = ' '
	Insert = '+'
	Remove = '-'


class Element(NamedTuple, Generic[T]):
	line: T
	operation: Operations


class Myers(Generic[T]):
	"""
		spotify playlist that are sorted by added_at can only have inserts
		at the bottom (most recently added). All inserts before that mean
		that a_lines doesnt have these items, which means for the sake of
		syncing, they should be removed from b_lines
	"""
	max_line_length = 0
	def __init__(self, a_lines: list[T]=[], b_lines: list[T]=[]):

		self._a_lines = [str(line) for line in a_lines]
		self._b_lines = [str(line) for line in b_lines]
		# self._a_lines = a_lines
		# self._b_lines = b_lines

		d = Differ()
		self._diff = d.compare(self._a_lines, self._b_lines)
		self.refactor()

		self.keeps: list[str] = []
		self.inserts: list[str] = []
		self.removals: list[str] = []


	def refactor(self):
		self.diff: list[Element[str]] = []
		for line in self._diff:
			operation = Operations(line[0])
			val = line[2:]
			if len(val) > self.max_line_length:
				self.max_line_length = len(val)
			wrapped = Element(val, operation)
			self.diff.append(wrapped)


	def separate_operations(self, after_index: int=0):
		for line, operation in self.diff[after_index:]:
			if operation == Operations.Keep:
				self.keeps.append(line)
			elif operation == Operations.Insert:
				self.inserts.append(line)
			elif operation == Operations.Remove:
				self.removals.append(line)

	@property
	def get_num_elems_after(self):
		counter = 0
		for _, operation in self.diff:
			if operation == Operations.Keep or operation == Operations.Insert:
				counter += 1
		return counter


	def has_something(self, something: Operations):
		for _, operation in self.diff:
			if operation == something:
				return True
		return False


	@property
	def first_keep_index(self):
		for i, elem in enumerate(self.diff):
			if elem.operation == Operations.Keep:
				return i
		return None


	@property
	def last_keep_index(self):
		for i, elem in enumerate(reversed(self.diff)):
			if elem.operation == Operations.Keep:
				return i
		return None


	def get_vis_diff(self, title: str='Difference'):
		arr: list[str] = []

		line_length = self.max_line_length + 2
		whole_length = line_length * 2 + 7

		formatter = lambda left, right: f'| {left.rjust(line_length)} | {right.ljust(line_length)} |'

		arr.append(whole_length*'-')
		arr.append(f'|{title.center(whole_length-2)}|')
		arr.append(whole_length*'-')
		for line, operation in self.diff:
			line = str(line)
			line = f'{operation.value} {line}'
			if operation == Operations.Keep:
				arr.append(formatter(line, line))
			elif operation == Operations.Insert:
				arr.append(formatter('', line))
			elif operation == Operations.Remove:
				arr.append(formatter(line, ''))
		arr.append(whole_length*'-')

		return arr


	def print_diff(self, title='Difference', print_fn=print):
		diff = self.get_vis_diff(title)
		self.print_groups(diff, print_fn=print_fn)


	@classmethod
	def print_groups(cls, *diffs: list[str], group_size=1, distance=2, print_fn=print):

		# FIX line length
		line_length = cls.max_line_length + 2
		whole_length = line_length * 2 + 7
		for n in range(0, len(diffs), group_size):
			group = diffs[n:n+group_size]
			zipped = list(zip_longest(*group, fillvalue=' '*whole_length))

			for long_line in zipped:
				delimiter = ' ' * distance
				print_fn(delimiter.join(long_line))

			if distance > 2:
				line_breaks = max(int(distance / 3) - 1, 0)
				print_fn('\n' * line_breaks)


def main():
	# try:
	# 	_, a_file, b_file = sys.argv
	# except ValueError:
	# 	print(sys.argv[0], '<FILE>', '<FILE>')
	# 	return 1

	# with open(a_file) as a_handle:
	# 	a_lines = [line.rstrip() for line in a_handle]

	# with open(b_file) as b_handle:
	# 	b_lines = [line.rstrip() for line in b_handle]

	# a_lines = ['1', '2', '3']
	# b_lines = ['a', '1', 'b', '2', '34']
	a_lines = list(range(10))
	b_lines = list(range(5, 20))
	# del a_lines[15:30]
	# del b_lines[-1]
	# a_lines.append('41')
	b_lines.append(20)

	myers = Myers(a_lines, b_lines)
	myers2 = Myers(b_lines, a_lines)

	# myers2.print_diff()
	myers2.separate_operations()
	print(myers.keeps)
	print(myers2.keeps)


if __name__ == '__main__':
	# sys.exit(main())
	main()