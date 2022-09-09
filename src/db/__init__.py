from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.db.session import create_session, engine, get_session

_: Session = None  # type: ignore
Base = declarative_base(bind=engine)

from src.db import helpers, playlists, tables, tracks

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
