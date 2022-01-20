def named_tuple():
	from typing import NamedTuple

	class Typed2(NamedTuple):
		data2_1: str
		data2_2: str
	class Typed(NamedTuple):
		data_1: str
		data_2: Typed2

		def __init__(self, **kwargs) -> None:
			self.data_2 = Typed2(**kwargs['data_2'])
		
	my_dict = {
		'data_1': 'asdf',
		'data_2': {
			'data2_1': '1234',
			'data2_2': '5678',
			'data2_3': '5678',
		}
	}

	typed_dict = Typed(**my_dict)

	print(typed_dict.data_1)
	# print(typed_dict.data_2)

def data_class():
	from dataclasses import dataclass

	@dataclass
	class Data2:
		data2_1: str
		data2_2: str

	@dataclass
	class Data:
		data_1: str
		data_2: Data2
		def __init__(self, **kwargs) -> None:
			self.data_1 = kwargs['data_1']
			self.data_2 = Data2(**kwargs['data_2'])


	my_dict = {
		'data_1': 'asdf',
		'data_2': {
			'data2_1': '1234',
			'data2_2': '5678',
			# 'data2_3': '5678',
		}
	}

	data = Data(**my_dict)

	# print(data.data_2.data2_1)
	print(data.data_1)
	print(data.data_2.data2_1)

if __name__ == '__main__':
	data_class()
	# named_tuple()