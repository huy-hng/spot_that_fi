from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///src/db/SpotifyData.db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


def create_session() -> Session:
	return SessionMaker.begin()

def get_session(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		with SessionMaker.begin() as session:
			session: Session
			return fn(session, *args, **kwargs)
	return wrapper

from .tables import *
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from . import features, helpers, playlists, tables, tracks
