# %%
from copy import copy, deepcopy
from dataclasses import dataclass, field
from functools import update_wrapper
from typing import Generic, NamedTuple, TypeVar


def named_tuple():
	from typing import NamedTuple

	class Typed2(NamedTuple):
		data2_1: str
		data2_2: str
	class Typed(NamedTuple):
		data_1: str
		data_2: Typed2
		
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

	@dataclass
	class A:
		l: list[int] = field(default_factory=list)
		l: list[int] = []

def metaclass():


	class TestMetaclass(type):
		def __new__(cls, name, bases, namespace: dict, **kwargs):
			print(name)
			print(bases)
			print(namespace)
			print(kwargs)
			print()
			return super().__new__(cls, name, bases, namespace, **kwargs)


def generic_namedtuples():
	from typing import _NamedTuple, NamedTupleMeta  # type: ignore

	T = TypeVar('T')

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
		from typing import _GenericAlias, _NamedTuple  # type: ignore
		assert bases[0] is NamedTuple

		if len(bases) > 1:
			generic_only = all([isinstance(base, _GenericAlias) for base in bases[1:]])
			if not generic_only:
				raise TypeError("Multiple inheritance with NamedTuple is not supported")


		return (_NamedTuple,)

	NamedTuple.__mro_entries__ = _namedtuple_mro_entries  # type: ignore

	class Test(NamedTuple, Generic[T]):
		a: T
		b: str
		c: str

		


def singleton_class():
	from functools import wraps
	global single
	single = 0
	
	def dec(fn):

		@wraps(fn)
		def wrapper(*args, **kwargs):
			global single
			if single == 0:
				single = 1
			else:
				single += 1

			print('inside dec')
			fn(*args, **kwargs)

			single = 0

		return wrapper


	class Context:
		def __init__(self):
			self.instance = None
		def __enter__(self):
			return 1
		def __exit__(self, type, value, traceback):
			...

	class Single:
		def __init__(self):
			self.single = None

		def __call__(self):
			if self.single != None:
				return self.single

			print('before', self.single)
			with Context() as f:
				self.single = f
				return f
				self.single = None
				print('after', self.single)

			
	s = Single()
	print(Single()())
	# print('outside', val)
			

	@dec
	def fn1():
		global single
		print(single)

	@dec
	def fn2():
		global single
		print(single)
		fn1()
		fn1()

	# fn2()
	

if __name__ == '__main__':
	singleton_class()
