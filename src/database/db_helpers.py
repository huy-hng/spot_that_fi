from functools import wraps

from sqlalchemy import literal
from sqlalchemy.orm import Session as sess
from sqlalchemy.orm.query import Query

from src.database import Session 
from src.database.tables import Playlist, Track, PlaylistTracksAssociation

from src.logger import log


# def create_session(function):
# 	@wraps(function)
# 	def wrapper(*args, **kwargs):
# 		with Session.begin() as session:
# 			session: sess = session
# 			result = function(session, *args, **kwargs)
# 		return result
# 	return wrapper


def does_exist(query: Query):
	with Session.begin() as session:
		exists = session.query(literal(True)).filter(query.exists()).scalar()
		return exists if exists else False

