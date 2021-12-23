from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, Session as sess
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:')
# engine = create_engine('sqlite:///src/database/SpotifyData.db')
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

class TestTable(Base):
	__tablename__ = 'test_table'

	id = Column(Integer, primary_key=True)

Base.metadata.create_all(bind=engine)

with Session.begin() as session:
	session: sess = session
	for i in range(5):
		row = TestTable()
		row.id = i
		session.add(row)

	fetched: TestTable = session.query(TestTable).get(1)
	
	print(fetched.id)
