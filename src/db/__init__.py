from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as session_type
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///src/db/SpotifyData.db')
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

def get_session(fn):
	@wraps
	def wrapper(*args, **kwargs):
		with Session.begin() as session:
			session: session_type
			fn(session, *args, **kwargs)
	return wrapper

from .tables import *
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from . import features, helpers, playlists, tables, tracks
