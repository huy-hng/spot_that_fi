from dataclasses import dataclass, is_dataclass
from types import GenericAlias


def init(self, d: dict):
	_init(self, d)
	recursively_set_fields(self, d)


def _init(self, d: dict):
	from dataclasses import _fields_in_init_order, _init_fn  # type: ignore
	all_init_fields = [f for f in self.__dataclass_fields__.values()]
	(std_init_fields,
		kw_only_init_fields) = _fields_in_init_order(all_init_fields)

	frozen = True
	has_post_init = False
	slots = True

	_init_fn(
		all_init_fields,
		std_init_fields,
		kw_only_init_fields,
		frozen,
		has_post_init,
		'self',
		{},
		slots,
	)(self, **d)


def recursively_set_fields(self, kwargs):
	for f in self.__dataclass_fields__.values():
		# if isinstance(field_.type == dataclass)
		if isinstance(f.type, GenericAlias):
			a = GenericAlias(list, (int,))
			# print(a.__args__)
			b = f.type
			# print(b.__args__[0])
			print(dir(b))
			for val in dir(b):
				print (val)

			# for k,v in b.__dict__.items():
			# 	print(k, v)
			# f.type 
		# if 'items' in f.name:
		# 	print(f.type)
			# print(len(f.type))
			# a = f.type(['1'])
			# print(a)
			# print(is_dataclass(f.type))
		if is_dataclass(f.type):
			v = kwargs.get(f.name)
			if v is None:
				continue

			try:
				v = f.type(v)
			except TypeError:
				v = f.type(**v)

			object.__setattr__(self, f.name, v)

# from . import playlists, tracks