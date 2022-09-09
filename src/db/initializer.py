from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
SessionMaker = sessionmaker()


db_path = 'sqlite:///database'
def get_production_engine():
	return create_engine(f'{db_path}/SpotifyData.db')


def get_testing_engine():
	return create_engine(f'{db_path}/Testing.db')


def get_memory_engine():
	return create_engine('sqlite:///:memory:')


def configure_db(engine: Engine):
	SessionMaker.configure(bind=engine)

	Base.metadata.bind = engine
	Base.metadata.create_all()


def delete_tables(engine):
	Base.metadata.drop_all()
	Base.metadata.create_all()
