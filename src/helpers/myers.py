# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <http://unlicense.org/> 

from enum import Enum
from typing import NamedTuple

# These define the structure of the history, and correspond to diff output with
# lines that start with a space, a + and a - respectively.

class Operations(Enum):
	Keep = ' '
	Insert = '+'
	Remove = '-'

class Element(NamedTuple):
	line: str
	operation: Operations


# See frontier in myers_diff
# Frontier = namedtuple('Frontier', ['x', 'history'])
class Frontier(NamedTuple):
	x: int
	history: list[Element]

def myers_diff(a_lines, b_lines) -> list[Element]:
	"""
	An implementation of the Myers diff algorithm.

	See http://www.xmailserver.org/diff2.pdf
	"""
	# This marks the farthest-right point along each diagonal in the edit
	# graph, along with the history that got it there
	frontier = {1: Frontier(0, [])}


	def one(idx):
		"""
		The algorithm Myers presents is 1-indexed; since Python isn't, we
		need a conversion.
		"""
		return idx - 1

	a_max = len(a_lines)
	b_max = len(b_lines)
	for d in range(0, a_max + b_max + 1):
		for k in range(-d, d + 1, 2):
			""" This determines whether our next search point will be going down
			in the edit graph, or to the right.
			
			The intuition for this is that we should go down if we're on the
			left edge (k == -d) to make sure that the left edge is fully
			explored.
			
			If we aren't on the top (k != d), then only go down if going down
			would take us to territory that hasn't sufficiently been explored
			yet. """
			go_down = (k == -d or 
					(k != d and frontier[k - 1].x < frontier[k + 1].x))

			""" Figure out the starting point of this iteration. The diagonal
			offsets come from the geometry of the edit grid - if you're going
			down, your diagonal is lower, and if you're going right, your
			diagonal is higher. """
			if go_down:
				old_x, history = frontier[k + 1]
				x = old_x
			else:
				old_x, history = frontier[k - 1]
				x = old_x + 1

			""" We want to avoid modifying the old history, since some other step
			may decide to use it. """
			history = history[:]
			y = x - k

			""" We start at the invalid point (0, 0) - we should only start building
			up history when we move off of it. """
			if 1 <= y <= b_max and go_down:
				# history.append(Insert(b_lines[one(y)]))
				elem = Element(b_lines[one(y)], Operations.Insert)
				history.append(elem)
			elif 1 <= x <= a_max:
				# history.append(Remove(a_lines[one(x)]))
				elem = Element(a_lines[one(x)], Operations.Remove)
				history.append(elem)

			""" Chew up as many diagonal moves as we can - these correspond to common lines,
			and they're considered "free" by the algorithm because we want to maximize
			the number of these in the output. """
			while x < a_max and y < b_max and a_lines[one(x + 1)] == b_lines[one(y + 1)]:
				x += 1
				y += 1
				# history.append(Keep(a_lines[one(x)]))
				elem = Element(a_lines[one(x)], Operations.Keep)
				history.append(elem)

			if x >= a_max and y >= b_max:
				""" If we're here, then we've traversed through the bottom-left corner,
				and are done. """
				return history
			else:
				frontier[k] = Frontier(x, history)

	assert False, 'Could not find edit script'


class Myers:
	"""
		spotify playlist that are sorted by added_at can only have inserts
		at the bottom (most recently added). All inserts before that mean
		that a_lines doesnt have these items, which means for the sake of
		syncing, they should be removed from b_lines
	"""
	def __init__(self, a_lines: list, b_lines: list):
		self.diff = myers_diff(a_lines, b_lines)
	
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
	def index_of_first_keep(self):
		for i, elem in enumerate(self.diff):
			if elem.operation == Operations.Keep:
				return i
		return None


	def separate_operations(self):
		keeps: list[str] = []
		inserts: list[str] = []
		removals: list[str] = []

		for line, operation in self.diff[self.index_of_first_keep:]:
			if operation == Operations.Keep:
				keeps.append(line)
			elif operation == Operations.Insert:
				inserts.append(line)
			elif operation == Operations.Remove:
				removals.append(line)

		return keeps, inserts, removals


	def print_diff(self, print_fn=print):
		printer = lambda left, right: print_fn(f'| {left.rjust(5)} | {right.ljust(4)} |')

		print_fn(16*'-')
		printer('old', 'new')
		for line, operation in self.diff:
			line = operation.value + line
			if operation == Operations.Keep:
				printer(line, line)
			elif operation == Operations.Insert:
				printer('', line)
			elif operation == Operations.Remove:
				printer(line, '')
		print_fn(16*'-')

		
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
	a_lines = [str(num) for num in range(40)]
	b_lines = [str(num) for num in range(20, 40)]
	# del a_lines[15:30]
	del b_lines[-1]
	a_lines.append('41')
	# b_lines.append('40')

	myers = Myers(a_lines, b_lines)
	# myers = Myers(b_lines, a_lines)
	myers.print_diff()
	

if __name__ == '__main__':
	# sys.exit(main())
	main()