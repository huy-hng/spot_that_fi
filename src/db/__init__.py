from functools import wraps
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as session_type
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///src/db/SpotifyData.db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

def get_session(function: Callable):
	# @wraps(function)
	def wrapper(*args, **kwargs):
		with SessionMaker.begin() as session:
			session: session_type
			result = function(session, *args, **kwargs)
		return result
	return wrapper

def get_session_fn(function):
	session: session_type = SessionMaker.begin()
	# with Session.begin() as session:
	# 	session: session_type

from .tables import *
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from . import features, helpers, playlists, tables, tracks
