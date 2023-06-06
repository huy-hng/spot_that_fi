from datetime import datetime
import time
from functools import wraps
import json
from typing import Callable, Generator, Iterable, TypeVar, NamedTuple


def allow_generic_namedtuples():
	def _namedtuple_mro_entries(bases):
		from typing import _GenericAlias, _NamedTuple  # type: ignore
		assert bases[0] is NamedTuple

		if len(bases) > 1:
			generic_only = all([isinstance(base, _GenericAlias) for base in bases[1:]])
			if not generic_only:
				raise TypeError(
					"Multiple inheritance with NamedTuple is not supported")

		return (_NamedTuple,)

	NamedTuple.__mro_entries__ = _namedtuple_mro_entries  # type: ignore


def timer(fn: Callable):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		start = time.perf_counter()
		result = fn(*args, **kwargs)
		end = time.perf_counter()
		print(f'{fn.__name__} took {end-start: 2f} seconds to execute.')
		return result
	return wrapper

def parse_time(time: str):
	# TODO: timezones?
	return datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')


def clamp(x: int, /, minimum: int, maximum: int):
	return max(minimum, min(maximum, x))


def write_data(name: str, data):
	with open(f'./data/{name}.json', 'w') as f:
		f.write(json.dumps(data, indent=2))


def read_data(name: str):
	with open(f'./data/{name}.json') as f:
		return json.load(f)


def create_data_class(data: dict):
	for k, v in data.items():
		print(f'{k}: {type(v).__name__}')
		type_ = type(v).__name__
		if type_ == 'list':
			print('=============')
			create_data_class(v[0])
		elif type_ == 'dict':
			print('=============')
			create_data_class(v)


T = TypeVar('T')


def lookahead(iterable: Iterable[T]) -> Generator[tuple[T, bool], None, None]:
	it = iter(iterable)
	try:
		last = next(it)
	except StopIteration:
		return

	else:
		for val in it:
			yield last, True
			last = val
		yield last, False


def grouper(x: list[T], /, group_size: int) -> list[list[T]]:
	""" 
	Args:
		x:
			the list to be grouped. Can only be passed positionally only
		group_size:
			size to be grouped
			if group_size == 0: return one group with all items
	"""
	group_size = min(group_size, len(x))

	if group_size == 0:
		group_size = len(x)

	return [x[n:n + group_size] for n in range(0, len(x), group_size)]


def print_dict(d: dict, print_fn=print):
	for k, v in d.items():
		print_fn(f'{k}: {v}')
	print_fn()


def print_list(l: list, print_fn=print):
	for v in l:
		print_fn(v)
	print_fn()


if __name__ == '__main__':
	with open('../data/playlists.json') as f:
		playlists = f.read()
	playlists = json.loads(playlists)
	create_data_class(playlists)