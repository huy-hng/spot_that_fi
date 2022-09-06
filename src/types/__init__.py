from dataclasses import is_dataclass
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
		value = kwargs.get(f.name)
		if value is None:
			continue

		if is_dataclass(f.type):
			try:
				value = f.type(value)
			except TypeError:
				value = f.type(**value)
		elif isinstance(f.type, GenericAlias):
			value = [f.type.__args__[0](item) for item in value]
		else:
			continue

		object.__setattr__(self, f.name, value)
