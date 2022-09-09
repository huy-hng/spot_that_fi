from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


_: Session = None  # type: ignore

db_path = 'sqlite:///database'
engine = create_engine('sqlite:///:memory:')
engine = create_engine(f'{db_path}/SpotifyData.db')
engine = create_engine(f'{db_path}/Testing.db')

Base = declarative_base()
SessionMaker = sessionmaker()

from src.db import tables
from src.db.session import create_session, get_session

def configure():
	Base.metadata.bind = engine
	SessionMaker.configure(bind=engine)

configure()  # engine has to be put in before the lines below
Base.metadata.drop_all()
Base.metadata.create_all()

from src.db import helpers, playlists, tracks
