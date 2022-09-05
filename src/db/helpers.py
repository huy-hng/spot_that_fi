from functools import wraps

from sqlalchemy import literal, exists
from sqlalchemy.orm import Session as sess
from sqlalchemy.orm.query import Query

from src.db import SessionMaker

from src.helpers.logger import log


def does_exist(query: Query):
	with SessionMaker.begin() as session:
		exists = session.query(literal(True)).filter(query.exists()).scalar()
		return exists if exists else False
