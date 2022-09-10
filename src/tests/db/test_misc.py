import random
from src import db
from src.db import create_session
from src.db.helpers import does_exist
# from src.db.tables import TestTable

def test_ordering():
	TestTable.__table__.drop()
	TestTable.__table__.create()

	# r = range(20, 0, -1)
	r = range(20)
	seen = []
	with create_session() as session:
		for i in r:
			# i = random.randint(0, 99)
			if i in seen:
				continue
			seen.append(i)

			print(i)
			row = TestTable(i)
			session.add(row)
