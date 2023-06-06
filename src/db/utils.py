from sqlalchemy import literal, exists
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from src.db import get_session, _

@get_session
def does_exist(query: Query, *, session: Session = _):
	exists = session.query(literal(True)).filter(query.exists()).scalar()
	return exists if exists else False
