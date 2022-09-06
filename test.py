# %%
from copy import copy, deepcopy
from dataclasses import dataclass, field
from typing import Generic, NamedTuple, TypeVar


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


T = TypeVar('T')


class TestMetaclass(type):
	def __new__(cls, name, bases, namespace: dict, **kwargs):
		print(name)
		print(bases)
		print(namespace)
		print(kwargs)
		print()
		return super().__new__(cls, name, bases, namespace, **kwargs)


from typing import _NamedTuple, NamedTupleMeta
class AllowGenericNamedTuple(type):
	@staticmethod
	def _namedtuple_mro_entries(bases):
		assert bases[0] is NamedTuple
		return (_NamedTuple,)

	def __new__(cls, name, bases, namespace: dict, **kwargs):
	
		# GenericNamedTuple = NamedTuple
		# GenericNamedTuple.__mro_entries__ = cls._namedtuple_mro_entries

		# bases = (GenericNamedTuple, *bases)
		print(bases)

		# namespace['__orig_bases__'] = Generic[T]

		# x = types.new_class(name, bases, **kwargs)
		x = super().__new__(cls, name, bases, namespace, **kwargs)

		return x
		# return super().__new__(cls, name, bases, namespace, **kwargs)
	def __init_subclass__(cls, a) -> None:
		super().__init_subclass__()


def _namedtuple_mro_entries(bases):
	from typing import _GenericAlias, _NamedTuple
	assert bases[0] is NamedTuple

	if len(bases) > 1:
		generic_only = all([isinstance(base, _GenericAlias) for base in bases[1:]])
		if not generic_only:
			raise TypeError("Multiple inheritance with NamedTuple is not supported")


	return (_NamedTuple,)

NamedTuple.__mro_entries__ = _namedtuple_mro_entries

class Test(NamedTuple, Generic[T]):
	a: T
	b: str
	c: str

		

@dataclass
class A:
	l: list[int] = field(default_factory=list)
	l: list[int] = []

if __name__ == '__main__':
	a1 = A()
	a2 = A()
	a2.l.append(1)
	print(a1.l)
	print(a2.l)
	
