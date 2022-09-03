import json
from typing import Iterable, TypeVar

def write_dict_to_file(name: str, data):
	with open(f'./data/{name}.json', 'w') as f:
		f.write(json.dumps(data, indent=2))

def read_dict_from_file(name: str):
	with open(f'./data/{name}.json') as f:
		return json.load(f)



def create_data_class(data: dict):
	for k,v in data.items():
		print(f'{k}: {type(v).__name__}')
		type_ = type(v).__name__
		if type_ == 'list':
			print('=============')
			create_data_class(v[0])
		elif type_ == 'dict':
			print('=============')
			create_data_class(v)


T = TypeVar('T')
def lookahead(iterable: Iterable[T]):
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


def grouper(x: list[T], /, group_size) -> list[list[T]]:
	""" 
	Args:
		x: the list to be grouped. Can only be passed positionally only
		group_size: size to be grouped
	"""
	group_size = min(group_size, len(x))

	if group_size == 0:
		group_size = len(x)

	return [x[n:n+group_size] for n in range(0, len(x), group_size)]

if __name__ == '__main__':
	with open('../data/playlists.json') as f:
		playlists = f.read()
	playlists = json.loads(playlists)
	create_data_class(playlists)
	