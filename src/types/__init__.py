# from typing import Protocol
# REFACTOR: use pydantic or something else that is more robust than this
class DotDict(dict):
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__

from . import playlists, tracks