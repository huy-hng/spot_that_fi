from functools import wraps

from sqlalchemy import literal
from sqlalchemy.orm import Session as sess
from sqlalchemy.orm.query import Query

from src.database import Session 

from src.helpers.logger import log


def does_exist(query: Query):
	with Session.begin() as session:
		exists = session.query(literal(True)).filter(query.exists()).scalar()
		return exists if exists else False


