from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, close_all_sessions


# engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///src/db/SpotifyData.db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)
scoped = scoped_session(SessionMaker)

_: Session = None

class SessionManager:
	session: Session = None

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

				cls.session = None
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
			cls.session = None
			return result
		return wrapper



def get_session(fn):
	@wraps(fn)
	def wrapper(*args, session=None, **kwargs):
		if session is not None:
			print(f'using passed session for {fn.__name__}')
			return fn(*args, session=session, **kwargs)
			
		with SessionMaker.begin() as session:
			print(f'creating new session for {fn.__name__}')
			return fn(*args, session=session, **kwargs)

	return wrapper



def create_session() -> Session:
	return SessionMaker.begin()


from .tables import *
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from . import features, helpers, playlists, tables, tracks
