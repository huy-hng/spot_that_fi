from functools import wraps
from inspect import signature
from typing import Callable

from sqlalchemy.orm import Session
from src.db.initializer import SessionMaker

_: Session = None  # type: ignore
_session: Session = None  # type: ignore
_parent_function: str = ''


def create_session() -> Session:
	return SessionMaker.begin()


def get_session(fn: Callable):
	requires_session = 'session' in signature(fn).parameters

	@wraps(fn)
	def wrapper(*args, **kwargs):
		global _session, _parent_function
		if 'session' in kwargs:
			# log.debug(f"using passed session for '{fn.__name__}'")
			return fn(*args, **kwargs)

		elif _session is not None:
			# log.debug(f"using '{_parent_function}' session for '{fn.__name__}'")

			if requires_session:
				kwargs['session'] = _session

			return fn(*args, **kwargs)

		_parent_function = fn.__name__
		with SessionMaker.begin() as session:
			_session = session
			# log.debug(f"creating new session for '{fn.__name__}'")

			if requires_session:
				kwargs['session'] = session

			result = fn(*args, **kwargs)

			_session = None  # type: None
			return result

	return wrapper


class SessionManager:
	session: Session = None  # type: ignore

	@classmethod
	def session_wrapper(cls, fn):
		@wraps(fn)
		def wrapper(*args, session: Session | None = None, **kwargs):
			if session is not None:
				print(f'passed session for {fn.__name__}')
				return fn(*args, **kwargs)

			if cls.session is not None:
				# kwargs['session'] = cls.session
				# print(f'using existing session for {fn.__name__}')
				return fn(*args, **kwargs)

			with SessionMaker.begin() as session_:
				# kwargs['session'] = session_
				# print(f'creating new session for {fn.__name__}')
				# print(id(session_))
				cls.session = session_
				result = fn(*args, **kwargs)

				cls.session = None  # type: ignore
				return result

		return wrapper

	@classmethod
	def new_session(cls, fn):
		@wraps(fn)
		def wrapper(*args, session: Session | None = None, **kwargs):
			print(f'creating new session for {fn.__name__}')
			with SessionMaker.begin() as session_:
				cls.session = session_
				result = fn(*args, **kwargs)
			cls.session = None  # type: ignore
			return result
		return wrapper
