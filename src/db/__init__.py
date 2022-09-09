from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# engine = create_engine('sqlite:///:memory:')
db_path = 'sqlite:///src/db/databases'
# engine = create_engine(f'{db_path}/Testing.db')
engine = create_engine(f'{db_path}/SpotifyData.db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)
_: Session = None  # type: ignore


def create_session() -> Session:
	return SessionMaker.begin()


def get_session(fn):
	@wraps(fn)
	def wrapper(*args, session=None, **kwargs):
		if session is not None:
			# print(f'using passed session for {fn.__name__}')
			return fn(*args, session=session, **kwargs)

		with SessionMaker.begin() as session:
			# print(f'creating new session for {fn.__name__}')
			return fn(*args, session=session, **kwargs)

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


from .tables import *

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
from . import features, helpers, playlists, tables, tracks
