from typing import Generic, NamedTuple, TypeVar
from src.utils import allow_generic_namedtuples

allow_generic_namedtuples()
T = TypeVar('T')

class Diff(NamedTuple, Generic[T]):
	inserts: list[T] = []
	removals: list[str] = []
